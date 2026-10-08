#!/usr/bin/env python3
"""
LDEV-6536: delete Docker Hub tags of lucee/lucee that are snapshot builds older than 90 days,
matching the Sonatype snapshot retention. Never touches release, RC, BETA or ALPHA tags.

Deletion only happens on or after 2027-03-01 (UTC), or with --force-delete for testing.
Before that it runs in dry-run mode and only logs what it would delete.

Needs DOCKERHUB_PRUNE_TOKEN: a Docker Hub Organization Access Token for the lucee org,
limited to the lucee/lucee repository, with the scope-tag-admin scope (read + delete tags).
The existing DOCKER_USERNAME / DOCKER_PASSWORD secrets are only used to push images and
cannot delete tags, so this has to be a separate secret.
"""

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ORG = os.getenv("DOCKERHUB_ORG", "lucee")
REPO = os.getenv("DOCKERHUB_REPO", "lucee")
CUTOFF = datetime.datetime(2027, 3, 1, tzinfo=datetime.timezone.utc)

# a snapshot build tag, including variant, tomcat/jdk and arch suffixes:
# 7.1.2.13-SNAPSHOT, 7.1.2.13-SNAPSHOT-light, 7.1.2.13-SNAPSHOT-light-nginx-tomcat11.0-jre25-temurin-noble-amd64
SNAPSHOT_TAG = re.compile(r"^\d+\.\d+\.\d+\.\d+-SNAPSHOT(-[A-Za-z0-9._-]+)?$")
NEVER_DELETE = re.compile(r"-(RC|BETA|ALPHA)(-|$)", re.IGNORECASE)


def log(message):
	print(message, flush=True)


class Hub:
	def __init__(self, token):
		self.token = token
		self.access = None

	def authenticate(self):
		body = json.dumps({"identifier": ORG, "secret": self.token}).encode()
		request = urllib.request.Request(
			"https://hub.docker.com/v2/auth/token", data=body,
			headers={"Content-Type": "application/json"})
		with urllib.request.urlopen(request, timeout=60) as response:
			self.access = json.load(response)["access_token"]

	def call(self, method, path):
		if self.access is None and self.token:
			self.authenticate()
		headers = {"Authorization": f"Bearer {self.access}"} if self.access else {}
		for attempt in range(6):
			request = urllib.request.Request(
				"https://hub.docker.com" + path, method=method, headers=headers)
			try:
				with urllib.request.urlopen(request, timeout=60) as response:
					raw = response.read()
					return response.status, json.loads(raw) if raw else {}
			except urllib.error.HTTPError as error:
				if error.code == 404 and method == "DELETE":
					return 404, {}  # already gone
				if error.code == 401 and attempt == 0 and self.token:
					self.authenticate()
					headers = {"Authorization": f"Bearer {self.access}"}
					continue
				if error.code == 429 or error.code >= 500:
					wait = int(error.headers.get("Retry-After", 2 ** attempt))
					log(f"hub returned {error.code}, retrying in {wait}s")
					time.sleep(wait)
					continue
				raise
		sys.exit(f"{method} {path} kept failing")


def tag_date(tag):
	value = tag.get("tag_last_pushed") or tag.get("last_updated")
	return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


def is_deletable(name, keep_version):
	if NEVER_DELETE.search(name) or "-SNAPSHOT" not in name:
		return False
	if not SNAPSHOT_TAG.match(name):
		return False
	if keep_version and (name == keep_version or name.startswith(keep_version + "-")):
		return False
	return True


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--max-age-days", type=int, default=90)
	parser.add_argument("--max-delete", type=int, default=1500)
	parser.add_argument("--dry-run", action="store_true", default=False,
		help="only log, never delete (this is also the default before 2027-03-01)")
	parser.add_argument("--force-delete", action="store_true", default=False,
		help="delete even before 2027-03-01")
	parser.add_argument("--name", default="SNAPSHOT",
		help="Docker Hub tag name filter (substring), e.g. 6.2.8.20-SNAPSHOT to look at one version")
	parser.add_argument("--keep-version", default=os.getenv("KEEP_VERSION", ""),
		help="snapshot version whose tags must not be deleted, e.g. the one just pushed")
	args = parser.parse_args()

	now = datetime.datetime.now(datetime.timezone.utc)
	dry_run = args.dry_run or not (args.force_delete or now >= CUTOFF)
	if dry_run and not args.dry_run:
		log(f"before {CUTOFF.date()} this only logs what it would delete (LDEV-6536)")
	limit = now - datetime.timedelta(days=args.max_age_days)
	log(f"{'dry run' if dry_run else 'deleting'}: -SNAPSHOT tags of {ORG}/{REPO} last pushed before {limit.date()}, up to {args.max_delete}")

	token = os.getenv("DOCKERHUB_PRUNE_TOKEN", "")
	if not token:
		if not dry_run:
			sys.exit("DOCKERHUB_PRUNE_TOKEN is not set, cannot delete tags")
		log("no DOCKERHUB_PRUNE_TOKEN, reading the tag list anonymously (only the oldest ~1000 tags can be paged)")
	hub = Hub(token)

	count = 0
	seen = 0
	page_number = 1
	while count < args.max_delete:
		# ordering=-last_updated returns the oldest tags first on this endpoint
		query = urllib.parse.urlencode({"page": page_number, "page_size": 100, "name": args.name, "ordering": "-last_updated"})
		try:
			status, page = hub.call("GET", f"/v2/namespaces/{ORG}/repositories/{REPO}/tags?{query}")
		except urllib.error.HTTPError as error:
			if dry_run and not token and error.code in (400, 403):
				log(f"stopping at page {page_number}: anonymous paging limit reached")
				break
			raise
		results = page.get("results", [])
		if page_number == 1 and "count" in page:
			log(f"{page['count']} tag(s) match '{args.name}'")
		if not results:
			break
		batch = []
		reached_recent = False
		for tag in results:
			seen += 1
			name = tag["name"]
			if not is_deletable(name, args.keep_version):
				log(f"skip {name} (not a snapshot build tag, or the version just built)")
				continue
			pushed = tag_date(tag)
			if pushed >= limit:
				reached_recent = True
				continue
			batch.append((name, pushed))
		for name, pushed in batch:
			if count >= args.max_delete:
				break
			if dry_run:
				log(f"would delete {name} (last pushed {pushed.date()})")
			else:
				log(f"deleting {name} (last pushed {pushed.date()})")
				hub.call("DELETE", f"/v2/namespaces/{ORG}/repositories/{REPO}/tags/{urllib.parse.quote(name, safe='')}")
				time.sleep(0.4)  # stay well below the Hub API rate limit
			count += 1
		if reached_recent or not page.get("next"):
			break
		if dry_run or not batch:
			# nothing was deleted, so the next page is the next set of tags
			page_number += 1
		# after deleting, page 1 holds the next oldest tags again

	summary = f"{count} snapshot tag(s) older than {args.max_age_days} days {'would be deleted' if dry_run else 'deleted'} (looked at {seen})"
	log(summary)
	if os.getenv("GITHUB_STEP_SUMMARY"):
		with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary_file:
			summary_file.write(f"### Docker Hub snapshot prune\n{summary}\n")


if __name__ == "__main__":
	main()
