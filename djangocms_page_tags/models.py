# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.extensions import PageExtension, TitleExtension
from cms.extensions.extension_pool import extension_pool
from cms.models import Page, Title
from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from taggit_autosuggest.managers import TaggableManager

from .utils import get_cache_key


@extension_pool.register
class PageTags(PageExtension):
    tags = TaggableManager()

    def copy_relations(self, oldinstance, language):
        """ Needed to copy tags when publishing page """
        self.tags.set(*oldinstance.tags.all())

    class Meta:
        verbose_name = _('Page tags (all languages)')


@extension_pool.register
class TitleTags(TitleExtension):
    tags = TaggableManager()

    def copy_relations(self, oldinstance, language):
        """ Needed to copy tags when publishing page """
        self.tags.set(*oldinstance.tags.all())

    class Meta:
        verbose_name = _('Page tags (language-dependent)')


# Cache cleanup when deleting pages / editing page extensions
@receiver(pre_delete, sender=Page)
def cleanup_page(sender, instance, **kwargs):
    site_id = instance.node.site_id
    key = get_cache_key(
        None, instance, '', site_id, False
    )
    cache.delete(key)


@receiver(pre_delete, sender=Title)
def cleanup_title(sender, instance, **kwargs):
    site_id = instance.page.node.site_id
    key = get_cache_key(
        None, instance.page, instance.language, site_id, True
    )
    cache.delete(key)


@receiver(post_save, sender=PageTags)
def cleanup_pagetags(sender, instance, **kwargs):
    site_id = instance.extended_object.node.site_id
    key = get_cache_key(
        None, instance.extended_object, '', site_id, False
    )
    cache.delete(key)


@receiver(post_save, sender=TitleTags)
def cleanup_titletags(sender, instance, **kwargs):
    site_id = instance.extended_object.page.node.site_id
    key = get_cache_key(
        None, instance.extended_object.page, instance.extended_object.language,
        site_id, True
    )
    cache.delete(key)
