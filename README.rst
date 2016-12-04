===================
djangocms-page-tags
===================

.. image:: https://img.shields.io/pypi/v/djangocms-page-tags.svg
        :target: https://pypi.python.org/pypi/djangocms-page-tags
        :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/nephila/djangocms-page-tags.svg
        :target: https://travis-ci.org/nephila/djangocms-page-tags
        :alt: Latest Travis CI build status

.. image:: https://img.shields.io/pypi/dm/djangocms-page-tags.svg
        :target: https://pypi.python.org/pypi/djangocms-page-tags
        :alt: Monthly downloads

.. image:: https://coveralls.io/repos/nephila/djangocms-page-tags/badge.png
        :target: https://coveralls.io/r/nephila/djangocms-page-tags
        :alt: Test coverage

Tagged pages for django CMS 3

Python: 2.7, 3.4, 3.5

Django: 1.8 to 1.10

django CMS: 3.2 to 3.4

.. warning:: Since version 0.5, the support for Python 2.6, Python 3.3, Django<1.8 and django CMS<3.2
             has been dropped

**********
Quickstart
**********

Install djangocms-page-tags::

    pip install djangocms-page-tags

Then add it to INSTALLED_APPS along with its dependencies::

    'taggit',
    'taggit_autosuggest',
    'djangocms_page_tags',

Add `taggit_autosuggest` to urlconf::

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


.. image:: https://d2weczhvl823v0.cloudfront.net/nephila/djangocms-page-tags/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

