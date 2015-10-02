#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import djangocms_page_tags

from setuptools import setup

version = djangocms_page_tags.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print('You probably want to also tag the version now:')
    print('  git tag -a %s -m "version %s"' % (version, version))
    print('  git push --tags')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='djangocms-page-tags',
    version=version,
    description='Tagged pages for django CMS 3',
    long_description=readme + '\n\n' + history,
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/nephila/djangocms-page-tags',
    packages=[
        'djangocms_page_tags',
    ],
    include_package_data=True,
    install_requires=(
        'django-cms>=3.0',
        'django-taggit>=0.11.2',
        'django-taggit-autosuggest',
        'django-classy-tags>=0.3.4.1',
    ),
    license='BSD',
    zip_safe=False,
    test_suite='cms_helper.run',
    keywords='djangocms-page-tags',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
