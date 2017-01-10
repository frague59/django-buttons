# -*- coding: utf-8 -*-
"""
Simple build tasks for :mod:`buttons` application
"""
from __future__ import unicode_literals, absolute_import
import os

from fabric import api

PROJECT_ROOT = '/home/fguerin/Boulot/workspace/projects/intranet.ville.tg/django-buttons'
version = '0.1'
revision = '1'

api.env.hosts = ['ulysse.ville.tg']


@api.task
def sphinx():
    """
    Full builds the docs from `buttons` tree

    :returns: Nothing
    """
    print ('DEBUG:: sphinx()')
    autogen()
    make()
    git_commit()
    git_pull_docs()
    display_docs()


@api.task
def autogen():
    """
    Auto-generates docs from `buttons` tree

    :returns: Nothing
    """
    print ('DEBUG:: autogen()')
    with api.lcd(PROJECT_ROOT):
        cmd = ('sphinx-apidoc -H %(project)s -V %(version)s -R %(version)s.%(revision)s '
               '-P -f -M -o ../docs/source ./%(module)s' % {'project': 'buttons',
                                                            'version': version,
                                                            'revision': revision,
                                                            'module': 'buttons'})
        print ('DEBUG:: autogen() cmd = %s' % cmd)
        api.local(cmd)


@api.task
def make():
    """
    Auto-generates docs from `buttons` tree

    :returns: Nothing
    """
    print ('DEBUG:: make()')
    with api.lcd(os.path.join(PROJECT_ROOT, 'docs')):
        cmd = 'make html'
        print ('DEBUG:: autogen() cmd = %s' % cmd)
        api.local(cmd)


@api.task
def git_commit():
    """
    Add, commit and push docs to Git tree

    :returns: Nothing
    """
    print ('DEBUG:: git_commit()')
    with api.lcd(os.path.join(PROJECT_ROOT, 'docs')):
        api.local('git add ./build')
        api.local('git commit -m "Update docs"')
        api.local('git push origin master')


@api.task
def git_pull_docs():
    """
    Pull docs on dev server

    :returns: Nothing
    """
    with api.cd('/var/git/django-buttons'):
        api.run('git pull')


@api.task
def display_docs():
    """
    Display docs on local machine

    :returns: Nothing
    """
    api.local('xdg-open http://ulysse.ville.tg/docs/django-buttons/')
