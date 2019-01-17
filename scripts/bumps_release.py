#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Updates the release numbers for the current project
"""
import json
import os
import sys
import argparse
import logging
import re
from copy import deepcopy

# region Constants
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DJANGO_SETTINGS_FILE = "buttons/__init__.py"
SPHINX_CONF_FILE = "docs/source/conf.py"
SONAR_FILE = "sonar-project.properties"
PACKAGES_FILES = None

LEVELS = (logging.FATAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
# endregion Constants


class UpdateException(Exception):
    """
    An error has append on updating version
    """


def split_release(version):
    try:
        major, minor, release = version.split(".")
    except ValueError:
        logging.fatal(
            'Version number "%s" does not respect the <MAJOR>.<MINOR>.<RELEASE> format.',
            version,
        )
        raise
    else:
        return major, minor, release


def update_django_settings(major: str, minor: str, release: str, dry_run: bool = True):
    """
    Updates the main django settings file

    :param major: Major version
    :param minor: Minor version
    :param release: Release number
    :param dry_run: If `True`, no operation performed
    :return: Nothing
    """
    if not DJANGO_SETTINGS_FILE:
        print("update_django_settings() no `DJANGO_SETTINGS_FILE` provided")

    version_re = re.compile(r"^__version__\s*=\s*VERSION\s*=\s*['\"][.\d\w]+['\"]$")
    version_format = '__version__ = VERSION = "{major}.{minor}.{release}"\n'

    old_row, new_row = None, None
    counter = 0

    # Reads and copy the file content
    with open(os.path.join(ROOT, DJANGO_SETTINGS_FILE), "r") as ifile:
        content = ifile.readlines()
    new_content = deepcopy(content)

    for counter, row in enumerate(content):
        logging.debug(
            "update_django_settings() a row has been found:\n%d %s", counter, row
        )
        searched = version_re.search(row)
        if searched:
            logging.debug(
                "update_django_settings() a *MATCHING* row has been found:\n%d %s",
                counter,
                row,
            )
            old_row = deepcopy(row)
            new_row = version_format.format(major=major, minor=minor, release=release)
            break

    if old_row and new_row:
        logging.info(
            "update_django_settings() old_row:\n%s\nnew_row:\n%s", old_row, new_row
        )

    if not dry_run and new_row and counter:
        new_content[counter] = new_row

        with open(os.path.join(ROOT, DJANGO_SETTINGS_FILE), "w") as ofile:
            ofile.writelines(new_content)
        logging.info('update_django_settings() "%s" updated.', DJANGO_SETTINGS_FILE)
        return

    raise UpdateException("An error has append on updating version")


def update_packages_json(major: str, minor: str, release: str, dry_run: bool = True):
    """
    Updates the packages.json file

    :param major: Major version
    :param minor: Minor version
    :param release: Release number
    :param dry_run: If `True`, no operation performed
    :return: Nothing
    """
    if not PACKAGES_FILES:
        print("update_django_settings() no `PACKAGES_FILES` provided")
        return

    if isinstance(PACKAGES_FILES, str):
        _PACKAGES_FILES = [PACKAGES_FILES]
    else:
        _PACKAGES_FILES = deepcopy(PACKAGES_FILES)

    for file in _PACKAGES_FILES:
        packages_file = os.path.join(ROOT, file)
        logging.info("update_packages_json() packages_file = %s", packages_file)
        try:
            with open(packages_file, "rw") as pf:
                packages = json.loads(pf.read())
                packages["version"] = ".".join([major, minor, release])
                updated = json.dumps(packages, indent=4)
                if not dry_run:
                    pf.write(updated)
        except IOError as ioe:
            raise UpdateException("Unable to perform packages[-lock].json update:", ioe)


def update_sphinx_conf(major: str, minor: str, release: str, dry_run: bool = True):
    """
    Updates the sphinx conf.py file

    :param major: Major version
    :param minor: Minor version
    :param release: Release number
    :param dry_run: If `True`, no operation performed
    :return: Nothing
    """
    if not SPHINX_CONF_FILE:
        print("update_sphinx_conf() no `SPHINX_CONF_FILE` provided")
        return

    version_re = re.compile(r"^version\s+=\s+[\"']([.\d]+)[\"']$")
    release_re = re.compile(r"^release\s+=\s+[\"']([.\d]+)[\"']$")

    version_format = 'version = "{major}.{minor}"\n'
    release_format = 'release = "{major}.{minor}.{release}"\n'

    old_version_row, old_release_row = None, None
    new_version_row, new_release_row = None, None

    # Reads and copy the file content
    with open(os.path.join(ROOT, SPHINX_CONF_FILE), "r") as ifile:
        content = ifile.readlines()
    new_content = deepcopy(content)

    # parse files
    counter_release, counter_version = 0, 0
    for counter, row in enumerate(content):
        # Searches for the "version" row
        version_searched = version_re.search(row)
        if version_searched:
            counter_version = counter
            old_version_row = deepcopy(row)
            new_version_row = version_format.format(major=major, minor=minor)
            continue

        # Searches for the "release" row
        release_searched = release_re.search(row)
        if release_searched:
            counter_release = counter
            old_release_row = deepcopy(row)
            new_release_row = release_format.format(
                major=major, minor=minor, release=release
            )
            continue

        if old_version_row and old_release_row and new_version_row and new_release_row:
            break

    if old_version_row and old_release_row:
        logging.info(
            "update_sphinx_conf() old_version_row:\n%s\nnew_version_row:\n%s",
            old_version_row,
            new_version_row,
        )

    if not dry_run and counter_version and counter_release:
        new_content[counter_version] = new_version_row
        new_content[counter_release] = new_release_row

        with open(os.path.join(ROOT, SPHINX_CONF_FILE), "w") as ofile:
            ofile.writelines(new_content)
        logging.info('update_sphinx_conf() "%s" updated.', SPHINX_CONF_FILE)
        return

    raise UpdateException("An error has append on updating version")


def update_sonar_properties(major: str, minor: str, release: str, dry_run: bool = True):
    """
    Updates the sonar-project.properties file

    :param major: Major version
    :param minor: Minor version
    :param release: Release number
    :param dry_run: If `True`, no operation performed
    :return: Nothing
    """
    if not SONAR_FILE:
        print("update_sonar_properties() no `SONAR_FILE` provided")
        return

    version_re = re.compile(r"^sonar.projectVersion=([.\d]+)$")
    version_format = "sonar.projectVersion={major}.{minor}\n"

    old_version_row, new_version_row = None, None

    with open(os.path.join(ROOT, SONAR_FILE), "r") as ifile:
        content = ifile.readlines()

    new_content = deepcopy(content)
    counter = 0

    for counter, row in enumerate(content):
        version_searched = version_re.search(row)
        if version_searched:
            old_version_row = deepcopy(row)
            new_version_row = version_format.format(major=major, minor=minor)
            break

    if old_version_row:
        logging.info(
            "update_sonar_properties() old_version_row:\n%s\nnew_version_row:\n%s",
            old_version_row,
            new_version_row,
        )

    if not dry_run:
        new_content[counter] = new_version_row
        with open(os.path.join(ROOT, SONAR_FILE), "w") as ofile:
            ofile.writelines(new_content)
        logging.info('update_sonar_properties() "%s" updated.', SONAR_FILE)
        return

    raise UpdateException("An error has append on updating version")


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(action="store", dest="version", help="Target release number")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store",
        dest="verbosity",
        default=0,
        help="Sets verbosity from 0 (quiet) to 4 (very verbose)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=False,
        help="Does not performs anything, displays the updates",
    )
    args = parser.parse_args(arguments)

    try:
        major, minor, release = split_release(args.version)
    except ValueError:
        return -1

    # Initialize the logger
    log_level = LEVELS[int(args.verbosity)]
    logging.basicConfig(level=log_level)

    # try:
    #     git_updater = GitReleaseUpdater(dry_run=args.dry_run)
    #     git_updater.update_release(major, minor, release)
    # except UpdateException as e:
    #     logging.fatal("Unable to update the GIT version:\n%s", e)
    #     return -32

    try:
        update_django_settings(major, minor, release, dry_run=args.dry_run)
    except UpdateException as e:
        logging.fatal("Unable to update the settings version:\n%s", e)
        return -2

    try:
        update_sphinx_conf(major, minor, release, dry_run=args.dry_run)
    except UpdateException as e:
        logging.fatal("Unable to update the docs version:\n%s", e)
        return -4

    try:
        update_sonar_properties(major, minor, release, dry_run=args.dry_run)
    except UpdateException as e:
        logging.fatal("Unable to update the sonar version:\n%s", e)
        return -8

    try:
        update_packages_json(major, minor, release, dry_run=args.dry_run)
    except UpdateException as e:
        logging.fatal("Unable to update the sonar version:\n%s", e)
        return -16

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
