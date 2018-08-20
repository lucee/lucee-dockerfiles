#!/usr/bin/env python3

from collections import namedtuple
import argparse
import subprocess
import os
import re
import yaml
import attr

@attr.s(frozen=True)
class Config(object):
	LUCEE_VERSION = attr.ib()
	LUCEE_SERVER = attr.ib()
	LUCEE_VARIANT = attr.ib()
	TOMCAT_VERSION = attr.ib()
	TOMCAT_JAVA_VERSION = attr.ib()
	TOMCAT_BASE_IMAGE = attr.ib()


def flatten(lst):
	return [x for y in lst for x in y]

def get_minor_version(ver):
	return re.sub(r"^(\d+\.\d+).*", r"\1", ver)

def run(cmd):
	return subprocess.run(cmd, check=True, universal_newlines=True)

def tomcat(config):
	return f"tomcat{config.TOMCAT_VERSION}-{config.TOMCAT_JAVA_VERSION}{config.TOMCAT_BASE_IMAGE}"

def discover_images():
	LUCEE_VERSIONS = os.getenv('LUCEE_VERSION').split(',')
	LUCEE_SERVERS = os.getenv('LUCEE_SERVER').split(',')
	LUCEE_VARIANTS = os.getenv('LUCEE_VARIANTS').split(',')
	TOMCAT_VERSION = os.getenv('TOMCAT_VERSION')
	TOMCAT_JAVA_VERSION = os.getenv('TOMCAT_JAVA_VERSION')
	TOMCAT_BASE_IMAGE = os.getenv('TOMCAT_BASE_IMAGE')

	for LUCEE_VERSION in LUCEE_VERSIONS:
		for LUCEE_SERVER in LUCEE_SERVERS:
			for LUCEE_VARIANT in LUCEE_VARIANTS:
				yield Config(
					LUCEE_VERSION=LUCEE_VERSION,
					LUCEE_SERVER=LUCEE_SERVER,
					LUCEE_VARIANT=LUCEE_VARIANT,
					TOMCAT_VERSION=TOMCAT_VERSION,
					TOMCAT_JAVA_VERSION=TOMCAT_JAVA_VERSION,
					TOMCAT_BASE_IMAGE=TOMCAT_BASE_IMAGE,
				)


def find_tags_for_image(config, default_tomcat, tags):
	yield f"{config.LUCEE_VERSION}{config.LUCEE_VARIANT}{config.LUCEE_SERVER}-{tomcat(config)}"

	is_default_tomcat = \
		config.TOMCAT_JAVA_VERSION == default_tomcat['TOMCAT_JAVA_VERSION'] and \
		config.TOMCAT_VERSION == default_tomcat['TOMCAT_VERSION'] and \
		config.TOMCAT_BASE_IMAGE == default_tomcat['TOMCAT_BASE_IMAGE']

	if is_default_tomcat:
		yield f"{config.LUCEE_VERSION}{config.LUCEE_VARIANT}{config.LUCEE_SERVER}"

	config_dict = attr.asdict(config)
	yield from [
		tag_name
		for tag_name, tag_requirements in tags.items()
		if all([config_dict[key] == tag_requirements[key] for key in set(config_dict.keys())])
	]


def config_to_build_args(config, namespace, image_name):
	if config.LUCEE_SERVER == '':
		build_args = {**attr.asdict(config), 'LUCEE_MINOR': get_minor_version(config.LUCEE_VERSION)}
	elif config.LUCEE_SERVER == '-nginx':
		build_args = {'LUCEE_IMAGE': f"{namespace}/{image_name}:{config.LUCEE_VERSION}{config.LUCEE_VARIANT}-{tomcat(config)}"}
	else:
		build_args = {}

	for key, value in build_args.items():
		yield from ['--build-arg', f"{key}={value}"]


def pick_dockerfile(config):
	if config.LUCEE_SERVER == '-nginx':
		if config.TOMCAT_BASE_IMAGE == '-alpine':
			return './Dockerfile.nginx.alpine'
		else:
			return './Dockerfile.nginx'
	else:
		return './Dockerfile'


def main():
	parser = argparse.ArgumentParser(description='Start the build process.')
	parser.add_argument('--no-build', dest='build', action='store_false', default=True,
						help='do not run the build')
	parser.add_argument('--no-push', dest='push', action='store_false', default=True,
						help='do not push the tags')
	parser.add_argument('--list-tags', action='store_true', default=False,
						help='only list the tags that would be generated')
	args = parser.parse_args()

	if args.list_tags:
		args.push = False
		args.build = False

	with open('./matrix.yaml') as matrix_file:
		matrix = yaml.safe_load(matrix_file)

	is_master_build = os.getenv('TRAVIS_PULL_REQUEST', None) == 'false'
	if os.getenv('CI', None):
		print('will we deploy:', 'yes' if is_master_build else 'no')

	namespace = matrix['config']['docker_hub_namespace']
	image_name = matrix['config']['docker_hub_image']

	for config in discover_images():
		build_args = list(config_to_build_args(config, namespace=namespace, image_name=image_name))
		dockerfile = pick_dockerfile(config)

		tags = find_tags_for_image(config, default_tomcat=matrix['default_tomcat'], tags=matrix['tags'])

		if args.list_tags:
			print(", ".join(tags))
			continue

		plain_tags = [f"{namespace}/{image_name}:{tag}" for tag in tags]
		tag_args = flatten([["-t", tag] for tag in plain_tags])
		command = [
			"docker", "build",
			*build_args,
			"-f", dockerfile,
			*tag_args,
			".",
		]

		print(' '.join(command))

		if args.build:
			run(command)

		for tag in plain_tags:
			if is_master_build and args.push:
				print('pushing', tag)
				run(["docker", "push", tag])
			else:
				print('not on master; skipping deployment of', tag)

if __name__ == '__main__':
	main()
