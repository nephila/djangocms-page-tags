#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from tempfile import mkdtemp


def gettext(s):
    return s


HELPER_SETTINGS = {
    'NOSE_ARGS': [
        '-s',
    ],
    'ROOT_URLCONF': 'tests.test_utils.urls',
    'INSTALLED_APPS': [
        'taggit',
        'taggit_autosuggest',
        'djangocms_page_tags',
        'tests.test_utils',
    ],
    'LANGUAGE_CODE': 'en',
    'LANGUAGES': (
        ('en', gettext('English')),
        ('fr_FR', gettext('French')),
        ('it', gettext('Italiano')),
    ),
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'en',
                'name': gettext('English'),
                'public': True,
            },
            {
                'code': 'it',
                'name': gettext('Italiano'),
                'public': True,
            },
            {
                'code': 'fr',
                'name': gettext('French'),
                'public': True,
            },
        ],
        'default': {
            'hide_untranslated': False,
        },
    },
    'CMS_TEMPLATES': (
        ('page_tags.html', 'page'),
    ),
    'FILE_UPLOAD_TEMP_DIR': mkdtemp()

}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_page_tags')

if __name__ == "__main__":
    run()
