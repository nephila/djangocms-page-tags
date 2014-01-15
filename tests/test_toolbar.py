# -*- coding: utf-8 -*-
"""
Tests for `djangocms_page_tags` modules module.
"""
from cms.toolbar.items import ModalItem, Menu
from cms.utils.compat.dj import force_unicode
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from . import BaseTest
from djangocms_page_tags.cms_toolbar import PAGE_TAGS_MENU_TITLE, TITLE_TAGS_MENU_TITLE
from djangocms_page_tags.models import PageTags, TitleTags


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
        Test that page menu is present if user has Page.change_perm
        """
        from cms.toolbar.toolbar import CMSToolbar
        page1, page2 = self.get_pages()
        self.user_staff.user_permissions.add(Permission.objects.get(codename='change_page'))
        self.user_staff = User.objects.get(pk=self.user_staff.pk)
        request = self.get_page_request(page1, self.user_staff, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')[0].item
        self.assertEqual(len(page_menu.find_items(ModalItem, name="%s ..." % force_unicode(PAGE_TAGS_MENU_TITLE))), 1)

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
        page1, page2 = self.get_pages()
        request = self.get_page_request(page1, self.user, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')[0].item
        self.assertEqual(len(page_menu.find_items(ModalItem, name="%s ..." % force_unicode(PAGE_TAGS_MENU_TITLE))), 1)
        self.assertEqual(len(page_menu.find_items(ModalItem, name="%s ..." % force_unicode(TITLE_TAGS_MENU_TITLE))), 1)

    def test_toolbar_with_items(self):
        """
        Test that PageTags/TitleTags items are present for superuser if PageTags/TitleTags exists for current page
        """
        from cms.toolbar.toolbar import CMSToolbar
        page1, page2 = self.get_pages()
        page_ext = PageTags.objects.create(extended_object=page1)
        title_ext = TitleTags.objects.create(extended_object=page1.get_title_obj('en'))
        request = self.get_page_request(page1, self.user, '/', edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name='Page')[0].item
        pagetags_menu = page_menu.find_items(ModalItem, name="%s ..." % force_unicode(PAGE_TAGS_MENU_TITLE))
        titletags_menu = page_menu.find_items(ModalItem, name="%s ..." % force_unicode(TITLE_TAGS_MENU_TITLE))
        self.assertEqual(len(pagetags_menu), 1)
        self.assertEqual(len(titletags_menu), 1)
        self.assertTrue(pagetags_menu[0].item.url.startswith(reverse('admin:djangocms_page_tags_pagetags_change', args=(page_ext.pk,))))
        self.assertTrue(titletags_menu[0].item.url.startswith(reverse('admin:djangocms_page_tags_titletags_change', args=(title_ext.pk,))))