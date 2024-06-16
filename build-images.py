#!/usr/bin/env python3

from collections import namedtuple
import argparse
import subprocess
import sys
import os
import re
import yaml
import attr
import requests
import xml.etree.ElementTree as ET

@attr.s(frozen=True)
class Config(object):
	LUCEE_MINOR = attr.ib()
	LUCEE_SERVER = attr.ib()
	LUCEE_VARIANT = attr.ib()
	TOMCAT_VERSION = attr.ib()
	TOMCAT_JAVA_VERSION = attr.ib()
	TOMCAT_BASE_IMAGE = attr.ib()

def flatten(lst):
	return [x for y in lst for x in y]

def is_release_build(ver):
	# builds with REBUILD_DATE should not apply plain tags
	# because they are typically older builds, not the latest
	if os.getenv('REBUILD_DATE', '') != '':
		return False

	# release builds are a version number string only
	# non-release builds contain a build type suffix such as -BETA/-RC/-SNAPSHOT
	return re.sub(r"^\d+\.\d+\.\d+\.\d+(.*)$", r"\1", ver) == ""

def get_minor_version(ver):
	return re.sub(r"^(\d+\.\d+).*", r"\1", ver)

def get_jar_url(ver, variant):
    print(f"Fetching URL for version: {ver} with variant: {variant}")
    
    if variant == '-light':
        return f"https://cdn.lucee.org/lucee-light-{ver}.jar"
    else:
        if "SNAPSHOT" in ver:
            try:
                return get_snapshot_url("org.lucee", "lucee", ver)
            except Exception as e:
                print(f"Error fetching snapshot URL from Sonatype: {e}. Falling back to CDN URL.")
                return f"https://cdn.lucee.org/lucee-{ver}.jar"
        else:
            try:
                return get_release_url("org.lucee", "lucee", ver)
            except Exception as e:
                print(f"Error fetching release URL from Sonatype: {e}. Falling back to CDN URL.")
                return f"https://cdn.lucee.org/lucee-{ver}.jar"


def run(cmd):
	return subprocess.run(cmd, check=True, universal_newlines=True)

def tomcat(config):
	return f"tomcat{config.TOMCAT_VERSION}-{config.TOMCAT_JAVA_VERSION}{config.TOMCAT_BASE_IMAGE}"

def rebuild_tag():
	if os.getenv('REBUILD_DATE', '') == '':
		return f""
	
	return f"-{os.getenv('REBUILD_DATE')}"


def discover_images():
	LUCEE_MINORS = os.getenv('LUCEE_MINOR').split(',')
	LUCEE_SERVERS = os.getenv('LUCEE_SERVER').split(',')
	LUCEE_VARIANTS = os.getenv('LUCEE_VARIANTS').split(',')
	TOMCAT_VERSION = os.getenv('TOMCAT_VERSION')
	TOMCAT_JAVA_VERSION = os.getenv('TOMCAT_JAVA_VERSION')
	TOMCAT_BASE_IMAGE = os.getenv('TOMCAT_BASE_IMAGE')

	for LUCEE_MINOR in LUCEE_MINORS:
		for LUCEE_SERVER in LUCEE_SERVERS:
			for LUCEE_VARIANT in LUCEE_VARIANTS:
				yield Config(
					LUCEE_MINOR=LUCEE_MINOR,
					LUCEE_SERVER=LUCEE_SERVER,
					LUCEE_VARIANT=LUCEE_VARIANT,
					TOMCAT_VERSION=TOMCAT_VERSION,
					TOMCAT_JAVA_VERSION=TOMCAT_JAVA_VERSION,
					TOMCAT_BASE_IMAGE=TOMCAT_BASE_IMAGE,
				)


def find_tags_for_image(config, default_tomcat, tags):
	yield f"{os.getenv('LUCEE_VERSION')}{config.LUCEE_VARIANT}{config.LUCEE_SERVER}-{tomcat(config)}{rebuild_tag()}"

	is_default_tomcat = \
		config.TOMCAT_JAVA_VERSION == default_tomcat['TOMCAT_JAVA_VERSION'] and \
		config.TOMCAT_VERSION == default_tomcat['TOMCAT_VERSION'] and \
		config.TOMCAT_BASE_IMAGE == default_tomcat['TOMCAT_BASE_IMAGE'] and \
		os.getenv('REBUILD_DATE', '') == ''

	if is_default_tomcat:
		yield f"{os.getenv('LUCEE_VERSION')}{config.LUCEE_VARIANT}{config.LUCEE_SERVER}"

	config_dict = attr.asdict(config)

	# only apply plain tags to release builds (exclude plain tags for non-release builds)
	if is_release_build(os.getenv('LUCEE_VERSION')):
		yield from [
			tag_name
			for tag_name, tag_requirements in tags.items()
			if all([config_dict[key] == tag_requirements[key] for key in set(config_dict.keys())])
		]


def config_to_build_args(config, namespace, image_name):
	if config.LUCEE_SERVER == '':
		build_args = {**attr.asdict(config), 'LUCEE_VERSION': os.getenv('LUCEE_VERSION'), 'LUCEE_MINOR': config.LUCEE_MINOR, 'LUCEE_JAR_URL': get_jar_url(os.getenv('LUCEE_VERSION'), config.LUCEE_VARIANT)}
	elif config.LUCEE_SERVER == '-nginx':
		build_args = {'LUCEE_IMAGE': f"{namespace}/{image_name}:{os.getenv('LUCEE_VERSION')}{config.LUCEE_VARIANT}-{tomcat(config)}{rebuild_tag()}"}
	else:
		build_args = {}

	for key, value in build_args.items():
		yield from ['--build-arg', f"{key}={value}"]


def pick_dockerfile(config):
	if config.LUCEE_SERVER == '-nginx':
		return './Dockerfile.nginx'
	else:
		return './Dockerfile'

# Determine if the version is a snapshot or a release, and call the appropriate function to get the artifact URL
def get_artifact_url(version):
    group_id = "org.lucee"
    artifact_id = "lucee"
    
    if "SNAPSHOT" in version:
        return get_snapshot_url(group_id, artifact_id, version)
    else:
        return get_release_url(group_id, artifact_id, version)

def get_snapshot_url(group_id, artifact_id, version):
    """
    Construct the URL for a snapshot version by reading the maven-metadata.xml file and extracting the correct snapshot version.
    """
    base_url = f"https://oss.sonatype.org/content/repositories/snapshots/{group_id.replace('.', '/')}/{artifact_id}/{version}/"
    metadata_url = base_url + "maven-metadata.xml"

    response = requests.get(metadata_url)
    print(f"Snapshot metadata URL: {metadata_url}, Status Code: {response.status_code}")
    if response.status_code != 200:
        raise Exception(f"Failed to access the URL: {metadata_url}")

    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()

    # Extract the value for the snapshot version with the jar extension
    snapshot_value = None
    for snapshot_version in root.findall('versioning/snapshotVersions/snapshotVersion'):
        extension = snapshot_version.findtext('extension')
        if extension == 'jar':
            snapshot_value = snapshot_version.findtext('value')
            break

    if not snapshot_value:
        raise Exception("No JAR file found in the snapshot versions.")

    jar_filename = f"{artifact_id}-{snapshot_value}.jar"
    jar_url = base_url + jar_filename

    return jar_url

def get_release_url(group_id, artifact_id, version):
    """
    Construct the URL for a release version and verify its existence using a HEAD request.
    """
    base_url = f"https://oss.sonatype.org/service/local/repositories/releases/content/{group_id.replace('.', '/')}/{artifact_id}/{version}/"
    jar_filename = f"{artifact_id}-{version}.jar?"
    jar_url = base_url + jar_filename

    # Make a HEAD request to check if the URL exists
    response = requests.head(jar_url)
    print(f"Release URL: {jar_url}, Status Code: {response.status_code}")
    if response.status_code == 200:
        return jar_url
    else:
        raise Exception(f"Release JAR not found at URL: {jar_url}")




def main():
	parser = argparse.ArgumentParser(description='Start the build process.')
	parser.add_argument('version', nargs='?', default=os.getenv('LUCEE_VERSION'),
						help='the version string to build (default: $LUCEE_VERSION)')
	parser.add_argument('--no-build', dest='build', action='store_false', default=True,
						help='do not run the build')
	parser.add_argument('--no-cache', dest='cache', action='store_false', default=True,
						help='do not use the cache when building')
	parser.add_argument('--no-push', dest='push', action='store_false', default=True,
						help='do not push the tags')
	parser.add_argument('--list-tags', action='store_true', default=False,
						help='only list the tags that would be generated')
	parser.add_argument('--buildx-platform', dest='platform', action='store', default='linux/amd64,linux/arm64',
						help='the target platform(s) to build, e.g. linux/amd64,linux/arm64')
	parser.add_argument('--buildx-load', dest='load', action='store_true', default=False,
						help='load the image into Docker from the builder')
	args = parser.parse_args()

	if args.list_tags:
		args.push = False
		args.build = False

	if os.getenv('LUCEE_TARGETPLATFORM', None):
		args.platform = os.getenv('LUCEE_TARGETPLATFORM', 'linux/amd64,linux/arm64')

	if args.load:
		args.push = False
		if ',' in args.platform:
			sys.exit("A single target platform must be specified when using load")


	if args.version == None:
		print("version argument missing or $LUCEE_VERSION not set")
		sys.exit(1)

	if os.getenv('SKIP_SNAPSHOTS', None):
		if "SNAPSHOT" in args.version:
			print("skipping SNAPSHOT build this run because SKIP_SNAPSHOTS env was set")
			sys.exit(0)


	with open('./matrix.yaml') as matrix_file:
		matrix = yaml.safe_load(matrix_file)

	is_master_build = os.getenv('DRY_RUN', 'false') != 'true'
	if os.getenv('CI', None):
		print('will we deploy:', 'yes' if is_master_build and args.push else 'no')

	namespace = matrix['config']['docker_hub_namespace']
	image_name = matrix['config']['docker_hub_image']

	for config in discover_images():
		if config.LUCEE_MINOR == get_minor_version(os.getenv('LUCEE_VERSION')):
			docker_args = ["--pull"]
			if args.load:
				# don't try to pull images from the registry when using buildx load
				docker_args = []

			if args.cache == False:
				docker_args.append("--no-cache")

			build_args = list(config_to_build_args(config, namespace=namespace, image_name=image_name))
			dockerfile = pick_dockerfile(config)

			tags = find_tags_for_image(config, default_tomcat=matrix['tags'][config.LUCEE_MINOR], tags=matrix['tags'])

			if args.list_tags:
				print(", ".join(tags))
				continue

			plain_tags = [f"{namespace}/{image_name}:{tag}" for tag in tags]
			tag_args = flatten([["-t", tag] for tag in plain_tags])

			buildx_args = []
			if args.load:
				buildx_args = [f"--load"]

			if is_master_build and args.push:
				buildx_args = [f"--push"]
				print('pushing', plain_tags)
			else: 
				print('not a master build; skipping deployment of', plain_tags)

			command = [
				"docker", "buildx", "build", *docker_args,
				*build_args,
				"--platform", args.platform,
				*buildx_args,
				"-f", dockerfile,
				*tag_args,
				*buildx_args,
				".",
			]

			print(' '.join(command))

			if args.build:
				run(command)
		else:
			print('mismatch of LUCEE_MINOR and LUCEE_VERSION: [', config.LUCEE_MINOR, '/', os.getenv('LUCEE_VERSION'), ']')


if __name__ == '__main__':
	main()
