# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.api import get_page_draft
from cms.toolbar.items import Break
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils import get_cms_setting
from cms.utils.i18n import get_language_object
from cms.utils.permissions import has_page_change_permission
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.translation import ugettext_lazy as _

from .models import PageTags, TitleTags

try:
    from cms.cms_toolbars import PAGE_MENU_SECOND_BREAK
except ImportError:
    from cms.cms_toolbar import PAGE_MENU_SECOND_BREAK

PAGE_TAGS_MENU_TITLE = _('Tags')
PAGE_TAGS_ITEM_TITLE = _('Common')


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
        can_change = (
            self.request.current_page
            and self.request.current_page.has_change_permission(self.request)
        )
        if has_global_current_page_change_permission or can_change:
            not_edit_mode = not self.toolbar.edit_mode
            tags_menu = self.toolbar.get_or_create_menu('page')
            super_item = tags_menu.find_first(Break, identifier=PAGE_MENU_SECOND_BREAK) + 1
            tags_menu = tags_menu.get_or_create_menu(
                'pagetags', PAGE_TAGS_MENU_TITLE, position=super_item
            )
            position = 0
            # Page tags
            try:
                page_extension = PageTags.objects.get(extended_object_id=self.page.pk)
            except PageTags.DoesNotExist:
                page_extension = None
            try:
                if page_extension:
                    url = reverse('admin:djangocms_page_tags_pagetags_change',
                                  args=(page_extension.pk,))
                else:
                    url = '%s?extended_object=%s' % (
                        reverse('admin:djangocms_page_tags_pagetags_add'),
                        self.page.pk)
            except NoReverseMatch:  # pragma: no cover
                # not in urls
                pass
            else:
                tags_menu.add_modal_item(PAGE_TAGS_ITEM_TITLE,
                                         url=url, disabled=not_edit_mode,
                                         position=position)
            # Title tags
            for title in self.page.title_set.all():
                try:
                    title_extension = TitleTags.objects.get(extended_object_id=title.pk)
                except TitleTags.DoesNotExist:
                    title_extension = None
                try:
                    if title_extension:
                        url = reverse('admin:djangocms_page_tags_titletags_change',
                                      args=(title_extension.pk,))
                    else:
                        url = '%s?extended_object=%s' % (
                            reverse('admin:djangocms_page_tags_titletags_add'),
                            title.pk)
                except NoReverseMatch:  # pragma: no cover
                    # not in urls
                    pass
                else:
                    position += 1
                    language = get_language_object(title.language)
                    tags_menu.add_modal_item(language['name'],
                                             url=url, disabled=not_edit_mode,
                                             position=position)
