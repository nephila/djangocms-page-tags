from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin
from django.conf import settings
from django.contrib import admin

from .models import PageTags, TitleTags


@admin.register(PageTags)
class PageTagsAdmin(PageExtensionAdmin):
    class Media:
        css = {"all": ("{}djangocms_page_tags/css/{}".format(settings.STATIC_URL, "djangocms_page_tags_admin.css"),)}


@admin.register(TitleTags)
class TitleTagsAdmin(TitleExtensionAdmin):
    class Media:
        css = {"all": ("{}djangocms_page_tags/css/{}".format(settings.STATIC_URL, "djangocms_page_tags_admin.css"),)}
