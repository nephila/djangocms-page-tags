# -*- coding: utf-8 -*-
from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin
from django.contrib import admin

from .models import PageTags, TitleTags


class PageTagsAdmin(PageExtensionAdmin):

    class Media:
        css = {
            'all': ('%sdjangocms_page_tags/css/%s' % (
                settings.STATIC_URL, "sdjangocms_page_tags.css"),)
        }
admin.site.register(PageTags, PageTagsAdmin)


class TitleTagsAdmin(TitleExtensionAdmin):

    class Media:
        css = {
            'all': ('%sdjangocms_page_tags/css/%s' % (
                settings.STATIC_URL, "sdjangocms_page_tags.css"),)
        }
admin.site.register(TitleTags, TitleTagsAdmin)