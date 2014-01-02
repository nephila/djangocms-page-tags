# -*- coding: utf-8 -*-
from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin
from django.contrib import admin

from .models import PageTags, TitleTags


class PageTagsAdmin(PageExtensionAdmin):
    pass
admin.site.register(PageTags, PageTagsAdmin)


class TitleTagsAdmin(TitleExtensionAdmin):
    pass
admin.site.register(TitleTags, TitleTagsAdmin)