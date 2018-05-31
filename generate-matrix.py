#!/usr/bin/env python3

import subprocess
import itertools
import argparse
import sys
import os
import yaml


def should_include_combo(combination, exclusions):
	for exclusion in exclusions:
		if all([combination[key] == exclusion[key] for key in set(exclusion.keys())]):
			return False

	return True


def find_all_matrix_rows(matrix):
	matrix_vars = matrix['matrix']

	for TOMCAT_VERSION in matrix_vars['TOMCAT_VERSION']:
		for TOMCAT_JAVA_VERSION in matrix_vars['TOMCAT_JAVA_VERSION']:
			for TOMCAT_BASE_IMAGE in matrix_vars['TOMCAT_BASE_IMAGE']:
				for LUCEE_VERSION in matrix_vars['LUCEE_VERSION']:
					for LUCEE_SERVER in matrix_vars['LUCEE_SERVER']:
						for LUCEE_VARIANT in matrix_vars['LUCEE_VARIANT']:
							yield {
								'TOMCAT_VERSION': TOMCAT_VERSION,
								'TOMCAT_JAVA_VERSION': TOMCAT_JAVA_VERSION,
								'TOMCAT_BASE_IMAGE': TOMCAT_BASE_IMAGE,
								'LUCEE_VERSION': LUCEE_VERSION,
								'LUCEE_SERVER': LUCEE_SERVER,
								'LUCEE_VARIANT': LUCEE_VARIANT,
							}


def combine_rows_by_tomcat(rows):
	def group_by_tomcat(row):
		return (row['TOMCAT_VERSION'], row['TOMCAT_JAVA_VERSION'], row['TOMCAT_BASE_IMAGE'])

	for tomcat, combination in itertools.groupby(rows, group_by_tomcat):
		result = {
			'TOMCAT_VERSION': tomcat[0],
			'TOMCAT_JAVA_VERSION': tomcat[1],
			'TOMCAT_BASE_IMAGE': tomcat[2],
			'LUCEE_VERSION': set(),
			'LUCEE_SERVER': set(),
			'LUCEE_VARIANT': set(),
		}

		for row in combination:
			result['LUCEE_VERSION'].add(str(row['LUCEE_VERSION']))
			result['LUCEE_SERVER'].add(str(row['LUCEE_SERVER']))
			result['LUCEE_VARIANT'].add(str(row['LUCEE_VARIANT']))

		yield result


def coalesce_combinations(combinations):
	for combo in combinations:
		lucee_versions = ",".join(sorted(combo['LUCEE_VERSION']))
		lucee_servers = ",".join(sorted(combo['LUCEE_SERVER']))
		lucee_variants = ",".join(sorted(combo['LUCEE_VARIANT']))

		yield {
			'TOMCAT_VERSION': combo['TOMCAT_VERSION'],
			'TOMCAT_JAVA_VERSION': combo['TOMCAT_JAVA_VERSION'],
			'TOMCAT_BASE_IMAGE': combo['TOMCAT_BASE_IMAGE'],
			'LUCEE_VERSION': lucee_versions,
			'LUCEE_SERVER': lucee_servers,
			'LUCEE_VARIANTS': lucee_variants,
		}


def combination_to_env_line(combo):
	return " ".join([f"{key}={value}" for key, value in combo.items()])


def main():
	parser = argparse.ArgumentParser(description='Start the build process.')
	parser.add_argument('--list-tags', action='store_true', default=False,
						help='only list the tags that would be generated')
	parser.add_argument('--dry-run', action='store_true', default=False,
						help='print the new travis config, but do not write it')
	parser.add_argument('--quiet', action='store_true', default=False,
						help='do not print the travis config')
	args = parser.parse_args()

	with open('./matrix.yaml') as matrix_input:
		matrix = yaml.safe_load(matrix_input)

	rows = [
		row
		for row in find_all_matrix_rows(matrix)
		if should_include_combo(row, matrix['exclusions'])
	]

	combinations = list(combine_rows_by_tomcat(rows))
	coalesced = list(coalesce_combinations(combinations))

	if args.list_tags:
		for row in coalesced:
			subprocess.run(
				["./build-images.py", "--list-tags"],
				universal_newlines=True,
				check=True,
				env={**row, 'PATH': os.getenv('PATH')},
			)
		return

	travis_env_rows = [combination_to_env_line(combo) for combo in coalesced]
	config = {
		**matrix['travis'],
		'env': {
			'matrix': travis_env_rows,
		},
	}

	conf_stringified = yaml.dump(config, default_flow_style=False, width=240, indent=2)

	if not args.quiet:
		print(conf_stringified)

	if not args.dry_run:
		with open('./.travis.yml', 'w') as travis_config:
			travis_config.write(conf_stringified)


if __name__ == '__main__':
	main()
