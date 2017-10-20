# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from distutils.core import setup

setup(
    name='django-buttons',
    packages=['django-buttons', ],
    version='0.2',
    description='An application providing some template tags to add buttons to pages',
    author='François GUÉRIN',
    author_email='fguerin@ville-tourcoing.fr',
    url='https://github.com/frague59/django-buttons',
    # download_url='https://gitlab.ville.tg/fguerin/',
    keywords=('django',
              'buttons',
              'bootstrap3'),
    classifiers=('Development Status :: 4 - Beta',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 ),
    requires=('django', 'django-fontawesome', 'django-appconf')
)
