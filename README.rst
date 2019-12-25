===================
djangocms-page-tags
===================

|Gitter| |PyPiVersion| |PyVersion| |Status| |TestCoverage| |CodeClimate| |License|

Tagged pages for django CMS 3

Python: 2.7, 3.5, 3.6, 3.7

Django: 1.11 to 2.2

django CMS: 3.6 to 3.7

.. warning:: Since version 0.8, the support for Python 3.4, django CMS < 3.6
             has been dropped.

.. warning:: Since version 0.7, the support for Python 3.4 and Django<1.11
             has been dropped.

**********
Quickstart
**********

Install djangocms-page-tags::

    pip install djangocms-page-tags

Then add it to INSTALLED_APPS along with its dependencies::

    'taggit',
    'taggit_autosuggest',
    'djangocms_page_tags',

Add ``taggit_autosuggest`` to urlconf::

    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),


Execute migration or syncdb::

    $ python manage.py syncdb

or::

    $ python manage.py migrate

*****
Usage
*****

You will find two new items in the toolbar Page menu:

* Title tags (per language)
* Page tags (global)

These items allows to add tags to ``Title`` and ``Page`` instances, respectively

************
Templatetags
************

``djangocms-page-tags`` allows showing tags using four templatetags

* ``include_page_tags``
* ``include_title_tags``
* ``page_tags``
* ``title_tags``

*************
Documentation
*************

For further documentation see https://djangocms-page-tags.readthedocs.io/

.. |Gitter| image:: https://img.shields.io/badge/GITTER-join%20chat-brightgreen.svg?style=flat-square
    :target: https://gitter.im/nephila/applications
    :alt: Join the Gitter chat

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/djangocms-page-sitemap.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-sitemap
    :alt: Latest PyPI version

.. |PyVersion| image:: https://img.shields.io/pypi/pyversions/djangocms-page-sitemap.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-page-sitemap
    :alt: Python versions

.. |Status| image:: https://img.shields.io/travis/nephila/djangocms-page-sitemap.svg?style=flat-square
    :target: https://travis-ci.org/nephila/djangocms-page-sitemap
    :alt: Latest Travis CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/djangocms-page-sitemap/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-page-sitemap?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/djangocms-page-sitemap.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-page-sitemap/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/djangocms-page-sitemap/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-page-sitemap
   :alt: Code Climate
