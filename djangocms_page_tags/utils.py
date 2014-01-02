# -*- coding: utf-8 -*-
from cms.templatetags.cms_tags import _get_cache_key, _get_page_by_untyped_arg
from cms.utils import get_language_from_request, get_cms_setting, get_site_id
from django.core.cache import cache

from .models import PageTags, TitleTags


def get_page_tags(page):
    """
    Retrieves all the tags for a Page instance.

    :param page: a Page instance

    :return list or queryset of attached tags
    """
    try:
        return page.pagetags.tags.all()
    except PageTags.DoesNotExist:
        return []


def page_has_tag(page, tag):
    """
    Check if a Page object is associated with the given tag.

    :param page: a Page instance
    :param tag: a Tag instance or a slug string.

    :return boolean: whether the Page instance has the given tag attached
    (False if no Page or no attached PageTags exists)
    """
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

    :return list or queryset of attached tags
    """
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

    :return boolean: whether the Title instance has the given tag attached
    (False if no Title or no attached TitleTags exists)
    """
    if hasattr(tag, 'slug'):
        slug = tag.slug
    else:
        slug = tag
    try:
        return page.get_title_obj(language=lang, fallback=False).titletags.tags.filter(slug=slug).exists()
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

    :return list of tags
    """
    site_id = get_site_id(site)
    if lang is None:
        lang = get_language_from_request(request)
    if title:
        cache_key = _get_cache_key('page_tags', page_lookup, lang, site_id) + '_type:tags_list'
    else:
        cache_key = _get_cache_key('title_tags', page_lookup, lang, site_id) + '_type:tags_list'
    tags_list = cache.get(cache_key)
    if not tags_list:
        page = _get_page_by_untyped_arg(page_lookup, request, site_id)
        if page:
            if title:
                tags_list = get_title_tags(page, lang)
            else:
                tags_list = get_page_tags(page)
            cache.set(cache_key, tags_list, get_cms_setting('CACHE_DURATIONS')['content'])
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

    :return list of tags attached to the given Title
    """
    return get_page_tags_from_request(request, page_lookup, lang, site, True)