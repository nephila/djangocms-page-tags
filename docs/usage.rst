#####
Usage
#####

********************************
Assigning tags to pages / titles
********************************

Tags can be assigned from the admin interface or the toolbar.

In the toolbar you will find two items in the ``Page`` menu:

* Title tags (per language): it allows to add tags to the current page language
* Page tags (global): it allows to add tags to the page in every language


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


page_tags and title_tags
========================

These templatetags pulls the tags for the given object and return them
in the context for using in the template. The list can also be saved as a
context variable for later use.

**Arguments:**

* ``page_lookup`` (see `page_lookup`_ for more information)
* ``language`` (optional)
* ``site`` (optional)


.. _page_lookup: http://django-cms.readthedocs.org/en/latest/advanced/templatetags.html#page-lookup