# -*- coding: utf-8 -*-
"""
Tests for `djangocms_page_tags` modules module.
"""
from __future__ import absolute_import, print_function, unicode_literals

from cms.toolbar.items import Menu, ModalItem, SubMenu
from cms.utils.i18n import get_language_object
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.utils.encoding import force_text

from djangocms_page_tags.cms_toolbar import PAGE_TAGS_ITEM_TITLE, PAGE_TAGS_MENU_TITLE
from djangocms_page_tags.models import PageTags, TitleTags

from . import BaseTest


class ToolbarTest(BaseTest):

    def test_no_page(self):
        """
        Test that no page menu is present if request not in a page
        """
        from cms.toolbar.toolbar import CMSToolbar
        request = self.get_page_request(None, self.user, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')
        self.assertEqual(page_menu, [])

    def test_no_perm(self):
        """
        Test that no page menu is present if user has no perm
        """
        from cms.toolbar.toolbar import CMSToolbar
        page1, page2 = self.get_pages()
        request = self.get_page_request(page1, self.user_staff, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')
        self.assertEqual(page_menu, [])

    def test_perm(self):
        """
        Test that page tags menu is present if user has Page.change_perm
        """
        from cms.toolbar.toolbar import CMSToolbar
        page1, page2 = self.get_pages()
        self.user_staff.user_permissions.add(Permission.objects.get(codename='change_page'))
        self.user_staff = User.objects.get(pk=self.user_staff.pk)
        request = self.get_page_request(page1, self.user_staff, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')[0].item
        tags_menu = page_menu.find_items(SubMenu, name=force_text(PAGE_TAGS_MENU_TITLE))[0].item
        try:
            self.assertEqual(len(tags_menu.find_items(ModalItem, name="{0}...".format(force_text(PAGE_TAGS_ITEM_TITLE)))), 1)
        except AssertionError:
            self.assertEqual(len(tags_menu.find_items(ModalItem, name="{0} ...".format(force_text(PAGE_TAGS_ITEM_TITLE)))), 1)

    @override_settings(CMS_PERMISSION=True)
    def test_perm_permissions(self):
        """
        Test that no page menu is present if user has general page Page.change_perm  but not permission on current page
        """
        from cms.toolbar.toolbar import CMSToolbar
        page1, page2 = self.get_pages()
        self.user_staff.user_permissions.add(Permission.objects.get(codename='change_page'))
        self.user_staff = User.objects.get(pk=self.user_staff.pk)
        request = self.get_page_request(page1, self.user_staff, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')
        self.assertEqual(page_menu, [])

    def test_toolbar(self):
        """
        Test that PageTags/TitleTags items are present for superuser
        """
        from cms.toolbar.toolbar import CMSToolbar
        NEW_CMS_LANGS = {
            1: [
                {
                    'code': 'en',
                    'name': 'English',
                    'public': True,
                },
                {
                    'code': 'it',
                    'name': 'Italiano',
                    'public': True,
                },
            ],
            'default': {
                'hide_untranslated': False,
            },
        }

        page1, page2 = self.get_pages()
        with self.settings(CMS_LANGUAGES=NEW_CMS_LANGS):
            request = self.get_page_request(page1, self.user, '/', edit=True)
            toolbar = CMSToolbar(request)
            toolbar.get_left_items()
            page_menu = toolbar.find_items(Menu, name='Page')[0].item
            tags_menu = page_menu.find_items(SubMenu, name=force_text(PAGE_TAGS_MENU_TITLE))[0].item
            try:
                self.assertEqual(len(tags_menu.find_items(ModalItem, name="{0}...".format(force_text(PAGE_TAGS_ITEM_TITLE)))), 1)
            except AssertionError:
                self.assertEqual(len(tags_menu.find_items(ModalItem, name="{0} ...".format(force_text(PAGE_TAGS_ITEM_TITLE)))), 1)
            self.assertEqual(len(tags_menu.find_items(ModalItem)), len(NEW_CMS_LANGS[1])+1)

    def test_toolbar_with_items(self):
        """
        Test that PageTags/TitleTags items are present for superuser if PageTags/TitleTags exists for current page
        """
        from cms.toolbar.toolbar import CMSToolbar
        page1, page2 = self.get_pages()
        page_ext = PageTags.objects.create(extended_object=page1)
        request = self.get_page_request(page1, self.user, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')[0].item
        tags_menu = page_menu.find_items(SubMenu, name=force_text(PAGE_TAGS_MENU_TITLE))[0].item
        try:
            pagetags_menu = tags_menu.find_items(ModalItem, name="{0}...".format(force_text(PAGE_TAGS_ITEM_TITLE)))
            self.assertEqual(len(pagetags_menu), 1)
        except AssertionError:
            pagetags_menu = tags_menu.find_items(ModalItem, name="{0} ...".format(force_text(PAGE_TAGS_ITEM_TITLE)))
            self.assertEqual(len(pagetags_menu), 1)
        self.assertEqual(len(pagetags_menu), 1)
        self.assertTrue(pagetags_menu[0].item.url.startswith(reverse('admin:djangocms_page_tags_pagetags_change', args=(page_ext.pk,))))
        for title in page1.title_set.all():
            language = get_language_object(title.language)
            try:
                titletags_menu = tags_menu.find_items(ModalItem, name='{0}...'.format(language['name']))
                self.assertEqual(len(titletags_menu), 1)
            except AssertionError:
                titletags_menu = tags_menu.find_items(ModalItem, name='{0} ...'.format(language['name']))
                self.assertEqual(len(titletags_menu), 1)
            try:
                title_ext = TitleTags.objects.get(extended_object_id=title.pk)
                self.assertTrue(titletags_menu[0].item.url.startswith(reverse('admin:djangocms_page_tags_titletags_change', args=(title_ext.pk,))))
            except TitleTags.DoesNotExist:
                self.assertTrue(titletags_menu[0].item.url.startswith(reverse('admin:djangocms_page_tags_titletags_add')))
