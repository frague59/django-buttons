# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
from distutils.core import setup
from setuptools import find_packages

# Loads the version from package
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from buttons import __version__ as version

setup(
    name='django-buttons',
    version=version,
    description='An application providing some template tags to add buttons to pages',
    author='François GUÉRIN',
    author_email='fguerin@ville-tourcoing.fr',
    url='https://github.com/frague59/django-buttons',
    license='MIT',
    keywords=['django', 'buttons', 'bootstrap3'],
    classifiers=['Development Status :: 4 - Beta',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 ],
    install_requires=['django', 'django-fontawesome', 'django-appconf'],

    # Source files
    packages=find_packages('.'),

    # Includes static files
    include_package_data=True,

)

