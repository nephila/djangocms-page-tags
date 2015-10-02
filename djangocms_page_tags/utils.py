# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def get_cache_key(request, page, lang, site_id, title):
    """
    Create the cache key for the current page and tag type
    """
    try:
        from cms.cache import _get_cache_key
        from cms.templatetags.cms_tags import _get_page_by_untyped_arg
    except ImportError:
        from cms.templatetags.cms_tags import _get_page_by_untyped_arg, _get_cache_key

    from cms.models import Page
    if not isinstance(page, Page):
        page = _get_page_by_untyped_arg(page, request, site_id)
    if not site_id:
        site_id = page.site_id
    if not title:
        return _get_cache_key('page_tags', page, '', site_id) + '_type:tags_list'
    else:
        return _get_cache_key('title_tags', page, lang, site_id) + '_type:tags_list'


def get_page_tags(page):
    """
    Retrieves all the tags for a Page instance.

    :param page: a Page instance

    :return: list or queryset of attached tags
    :type: List
    """
    from .models import PageTags
    try:
        return page.pagetags.tags.all()
    except PageTags.DoesNotExist:
        return []


def page_has_tag(page, tag):
    """
    Check if a Page object is associated with the given tag.

    :param page: a Page instance
    :param tag: a Tag instance or a slug string.

    :return: whether the Page instance has the given tag attached (False if no Page or no
             attached PageTags exists)
    :type: Boolean
    """
    from .models import PageTags
    if hasattr(tag, 'slug'):
        slug = tag.slug
    else:
        slug = tag
    try:
        return page.pagetags.tags.filter(slug=slug).exists()
    except PageTags.DoesNotExist:
        return False


def get_title_tags(page, lang):
    """
    Retrieves all the tags for a Title (given as page and language).
    This function does not use fallbacks to retrieve title object.

    :param page: a Page instance
    :param lang: a language code

    :return: list or queryset of attached tags
    :type: List
    """
    from .models import TitleTags
    try:
        return page.get_title_obj(language=lang, fallback=False).titletags.tags.all()
    except TitleTags.DoesNotExist:
        return []


def title_has_tag(page, lang, tag):
    """
    Check if a Title object is associated with the given tag.
    This function does not use fallbacks to retrieve title object.

    :param page: a Page instance
    :param lang: a language code
    :param tag: a Tag instance or a slug string.

    :return: whether the Title instance has the given tag attached (False if no Title or no
             attached TitleTags exists)
    :type: Boolean
    """
    from .models import TitleTags
    if hasattr(tag, 'slug'):
        slug = tag.slug
    else:
        slug = tag
    try:
        return page.get_title_obj(
            language=lang, fallback=False
        ).titletags.tags.filter(slug=slug).exists()
    except TitleTags.DoesNotExist:
        return False


def get_page_tags_from_request(request, page_lookup, lang, site, title=False):
    """
    Get the list of tags attached to a Page or a Title from a request  from usual
    `page_lookup` parameters.

    :param request: request object
    :param page_lookup: a valid page_lookup argument
    :param lang: a language code
    :param site: a site id
    :param title: a boolean to extract the Page (if False) or Title instance

    :return: list of tags
    :type: List
    """
    from cms.templatetags.cms_tags import _get_page_by_untyped_arg
    from cms.utils import get_language_from_request, get_cms_setting, get_site_id
    from django.core.cache import cache

    site_id = get_site_id(site)
    if lang is None:
        lang = get_language_from_request(request)
    cache_key = get_cache_key(request, page_lookup, lang, site, title)
    tags_list = cache.get(cache_key)
    if not tags_list:
        page = _get_page_by_untyped_arg(page_lookup, request, site_id)
        if page:
            if title:
                tags_list = get_title_tags(page, lang)
            else:
                tags_list = get_page_tags(page)
            cache.set(cache_key, tags_list, timeout=get_cms_setting('CACHE_DURATIONS')['content'])
    if not tags_list:
        tags_list = ()
    return tags_list


def get_title_tags_from_request(request, page_lookup, lang, site):
    """
    Get the list of tags attached to a Title from a request from usual
    `page_lookup` parameters.

    :param request: request object
    :param page_lookup: a valid page_lookup argument
    :param lang: a language code
    :param site: a site id

    :return: list of tags attached to the given Title
    :type: List
    """
    return get_page_tags_from_request(request, page_lookup, lang, site, True)
