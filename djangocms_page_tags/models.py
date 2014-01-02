# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from taggit_autosuggest.managers import TaggableManager
from cms.extensions import PageExtension, TitleExtension
from cms.extensions.extension_pool import extension_pool


class PageTags(PageExtension):
    tags = TaggableManager()

    def copy_relations(self, oldinstance):
        """ Needed to copy tags when publishing page """
        self.tags.set(*oldinstance.tags.all())
extension_pool.register(PageTags)


class TitleTags(TitleExtension):
    tags = TaggableManager()

    def copy_relations(self, oldinstance):
        """ Needed to copy tags when publishing page """
        self.tags.set(*oldinstance.tags.all())
extension_pool.register(TitleTags)
