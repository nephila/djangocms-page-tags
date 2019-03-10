# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin
from django.conf import settings
from django.contrib import admin

from .models import PageTags, TitleTags


@admin.register(PageTags)
class PageTagsAdmin(PageExtensionAdmin):

    class Media:
        css = {
            'all': ('%sdjangocms_page_tags/css/%s' % (
                settings.STATIC_URL, 'djangocms_page_tags_admin.css'),)
        }


@admin.register(TitleTags)
class TitleTagsAdmin(TitleExtensionAdmin):

    class Media:
        css = {
            'all': ('%sdjangocms_page_tags/css/%s' % (
                settings.STATIC_URL, 'djangocms_page_tags_admin.css'),)
        }
