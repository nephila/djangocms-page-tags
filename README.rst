=============================
djangocms-page-tags
=============================

.. image:: https://badge.fury.io/py/djangocms-page-tags.png
    :target: http://badge.fury.io/py/djangocms-page-tags
    
.. image:: https://travis-ci.org/nephila/djangocms-page-tags.png?branch=master
        :target: https://travis-ci.org/nephila/djangocms-page-tags

.. image:: https://pypip.in/d/djangocms-page-tags/badge.png
        :target: https://pypi.python.org/pypi/djangocms-page-tags?version=latest

.. image:: https://coveralls.io/repos/nephila/djangocms-page-tags/badge.png?branch=master
        :target: https://coveralls.io/r/nephila/djangocms-page-tags?branch=master


Tagged pages for django CMS 3


Quickstart
----------

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


Usage
-----

You will find two new items in the toolbar Page menu:

* Title tags (per language)
* Page tags (global)

These items allows to add tags to ``Title`` and ``Page`` instances, respectively

Templatetags
------------

``djangocms-page-tags`` allows showing tags using four templatetags

* ``include_page_tags``
* ``include_title_tags``
* ``page_tags``
* ``title_tags``


.. image:: https://d2weczhvl823v0.cloudfront.net/nephila/djangocms-page-tags/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

