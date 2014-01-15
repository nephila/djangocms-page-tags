# -*- coding: utf-8 -*-
from cms.toolbar.items import ModalItem
from cms.api import get_page_draft
from cms.utils import get_cms_setting
from cms.utils.permissions import has_page_change_permission
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from .models import PageTags, TitleTags


PAGE_TAGS_MENU_TITLE = _('Page tags (global)')
TITLE_TAGS_MENU_TITLE = _('Title tags (per language)')

@toolbar_pool.register
class PageTagsToolbar(CMSToolbar):
    def populate(self):
        # always use draft if we have a page
        self.page = get_page_draft(self.request.current_page)

        if not self.page:
            # Nothing to do
            return

        # check global permissions if CMS_PERMISSIONS is active
        if get_cms_setting('PERMISSION'):
            has_global_current_page_change_permission = has_page_change_permission(self.request)
        else:
            has_global_current_page_change_permission = False
            # check if user has page edit permission
        can_change = self.request.current_page and self.request.current_page.has_change_permission(self.request)
        if has_global_current_page_change_permission or can_change:
            not_edit_mode = not self.toolbar.edit_mode
            current_page_menu = self.toolbar.get_or_create_menu('page')
            advanced = current_page_menu.find_first(ModalItem, url=reverse('admin:cms_page_advanced', args=(self.page.pk,)))
            # Page tags
            try:
                page_extension = PageTags.objects.get(extended_object_id=self.page.id)
            except PageTags.DoesNotExist:
                page_extension = None
            try:
                if page_extension:
                    url = reverse('admin:djangocms_page_tags_pagetags_change',
                                  args=(page_extension.pk,))
                else:
                    url = "%s?extended_object=%s" % (
                        reverse('admin:djangocms_page_tags_pagetags_add'),
                        self.page.pk)
            except NoReverseMatch:
                # not in urls
                pass
            else:
                current_page_menu.add_modal_item(PAGE_TAGS_MENU_TITLE,
                                                 url=url, disabled=not_edit_mode,
                                                 position=advanced)
            # Title tags
            try:
                title_extension = TitleTags.objects.get(extended_object_id=self.page.id)
            except TitleTags.DoesNotExist:
                title_extension = None
            try:
                if title_extension:
                    url = reverse('admin:djangocms_page_tags_titletags_change',
                                  args=(title_extension.pk,))
                else:
                    url = "%s?extended_object=%s" % (
                        reverse('admin:djangocms_page_tags_titletags_add'),
                        self.page.pk)
            except NoReverseMatch:
                # not in urls
                pass
            else:
                current_page_menu.add_modal_item(TITLE_TAGS_MENU_TITLE,
                                                 url=url, disabled=not_edit_mode,
                                                 position=advanced)
