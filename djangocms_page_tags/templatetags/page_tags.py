# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag, InclusionTag
from django import template

from ..utils import get_page_tags_from_request

register = template.Library()


class IncludePageTagsList(InclusionTag):
    template = 'djangocms_page_tags/templatetags/page_tags.html'
    name = 'include_page_tags'
    title = False

    options = Options(
        Argument('page_lookup'),
        Argument('lang', required=False, default=None),
        Argument('site', required=False, default=None),
    )

    def get_context(self, context, page_lookup, lang, site):
        request = context.get('request', False)
        if not request:  # pragma: no cover
            return {'tags_list': ''}
        tags_list = get_page_tags_from_request(request, page_lookup, lang, site,
                                               self.title)
        if tags_list:
            return {'tags_list': tags_list}
        return {'tags_list': ''}
register.tag(IncludePageTagsList)


class IncludeTitleTagsList(IncludePageTagsList):
    template = 'djangocms_page_tags/templatetags/title_tags.html'
    name = 'include_title_tags'
    title = True
register.tag(IncludeTitleTagsList)


class PageTagsList(AsTag):
    name = 'page_tags'
    title = False

    options = Options(
        Argument('page_lookup'),
        Argument('lang', required=False, default=None),
        Argument('site', required=False, default=None),
        'as',
        Argument('varname', required=True, resolve=False)
    )

    def get_value(self, context, page_lookup, lang, site):
        request = context.get('request', False)
        if not request:  # pragma: no cover
            return ''
        return get_page_tags_from_request(request, page_lookup, lang, site,
                                          self.title)
register.tag(PageTagsList)


class TitleTagsList(PageTagsList):
    name = 'title_tags'
    title = True
register.tag(TitleTagsList)
