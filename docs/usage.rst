#####
Usage
#####

********************************
Assigning tags to pages / titles
********************************

Tags can be assigned from the admin interface or the toolbar.


In the toolbar you will find a ``Tags`` submenu in the ``Page`` menu, with two
or more sub-items:

* Common: it allows to edit page-wide (language independent) tags;
* One entry per active language to edit language dependent tags.


*******************************
Retrieving tags in the template
*******************************

``djangocms-page-tags`` provides both a tag and an inclusion tag for each object.


include_page_tags and include_title_tags
========================================

These templatetags retrieve the tags for the given object and render them
according to the relative template
(``djangocms_page_tags/template/page_tags.html`` and
``djangocms_page_tags/template/title_tags.html``) respectively.

You can override the template using the standard django mechanism.
Tags are available in the context variable ``tags_list``.

**Arguments:**

* ``page_lookup`` (see `page_lookup`_ for more information)
* ``language`` (optional)
* ``site`` (optional)

For performance reason is advisable to always use a Page object as
``page_lookup`` parameter.

page_tags and title_tags
========================

These templatetags pulls the tags for the given object and save them in
the ``varname`` context variable.

**Arguments:**

* ``page_lookup`` (see `page_lookup`_ for more information)
* ``language`` (optional)
* ``site`` (optional)
* ``varname`` (required)

For performance reason is advisable to always use a Page object as
``page_lookup`` parameter.


.. _page_lookup: http://django-cms.readthedocs.org/en/latest/advanced/templatetags.html#page-lookup