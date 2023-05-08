"""
Tests for `djangocms_page_tags` modules module.
"""
from cms.toolbar.items import Menu, ModalItem, SubMenu
from cms.utils.i18n import get_language_object
from django.contrib.auth.models import Permission, User
from django.test.utils import override_settings
from django.urls import reverse
from django.utils.encoding import force_str

from djangocms_page_tags.cms_toolbars import PAGE_TAGS_ITEM_TITLE, PAGE_TAGS_MENU_TITLE
from djangocms_page_tags.models import PageTags, TitleTags

from . import BaseTest


class ToolbarTest(BaseTest):
    def test_no_page(self):
        """
        Test that no page menu is present if request not in a page
        """
        from cms.toolbar.toolbar import CMSToolbar

        request = self.get_page_request(None, self.user, "/", edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name="Page")
        self.assertEqual(page_menu, [])

    def test_no_perm(self):
        """
        Test that no page menu is present if user has no perm
        """
        from cms.toolbar.toolbar import CMSToolbar

        page1, page2 = self.get_pages()
        request = self.get_page_request(page1, self.user_staff, "/", edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name="Page")
        try:
            self.assertEqual(page_menu, [])
        except AssertionError:
            tags_menu = page_menu[0].item.find_items(SubMenu, name=force_str(PAGE_TAGS_MENU_TITLE))
            self.assertEqual(tags_menu, [])

    def test_page_types(self):
        """
        Test that page meta menu is not displayed on page types.
        """
        from cms.toolbar.toolbar import CMSToolbar

        page1, page2 = self.get_pages()
        page1.is_page_type = True
        page1.save()
        self.user_staff.user_permissions.add(Permission.objects.get(codename="change_page"))
        self.user_staff = User.objects.get(pk=self.user_staff.pk)
        request = self.get_page_request(page1, self.user_staff, "/", edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name="Page")[0].item
        page_items = page_menu.find_items(SubMenu, name=force_str(PAGE_TAGS_MENU_TITLE))
        self.assertEqual(len(page_items), 0)

    def test_perm(self):
        """
        Test that page tags menu is present if user has Page.change_perm
        """
        from cms.toolbar.toolbar import CMSToolbar

        page1, page2 = self.get_pages()
        self.user_staff.user_permissions.add(Permission.objects.get(codename="change_page"))
        self.user_staff = User.objects.get(pk=self.user_staff.pk)
        request = self.get_page_request(page1, self.user_staff, "/", edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name="Page")[0].item
        tags_menu = page_menu.find_items(SubMenu, name=force_str(PAGE_TAGS_MENU_TITLE))[0].item
        self.assertEqual(len(tags_menu.find_items(ModalItem, name="{}...".format(force_str(PAGE_TAGS_ITEM_TITLE)))), 1)

    @override_settings(CMS_PERMISSION=True)
    def test_perm_permissions(self):
        """
        Test that no page menu is present if user has general page Page.change_perm  but not permission on current page
        """
        from cms.toolbar.toolbar import CMSToolbar

        page1, page2 = self.get_pages()
        self.user_staff.user_permissions.add(Permission.objects.get(codename="change_page"))
        self.user_staff = User.objects.get(pk=self.user_staff.pk)
        request = self.get_page_request(page1, self.user_staff, "/", edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name="Page")
        try:
            self.assertEqual(page_menu, [])
        except AssertionError:
            tags_menu = page_menu[0].item.find_items(SubMenu, name=force_str(PAGE_TAGS_MENU_TITLE))
            self.assertEqual(tags_menu, [])

    def test_toolbar(self):
        """
        Test that PageTags/TitleTags items are present for superuser
        """
        from cms.toolbar.toolbar import CMSToolbar

        NEW_CMS_LANGS = {  # noqa: N806
            1: [
                {
                    "code": "en",
                    "name": "English",
                    "public": True,
                },
                {
                    "code": "it",
                    "name": "Italiano",
                    "public": True,
                },
            ],
            "default": {
                "hide_untranslated": False,
            },
        }

        page1, page2 = self.get_pages()
        with self.settings(CMS_LANGUAGES=NEW_CMS_LANGS):
            request = self.get_page_request(page1, self.user, "/", edit=True)
            toolbar = CMSToolbar(request)
            toolbar.get_left_items()
            page_menu = toolbar.find_items(Menu, name="Page")[0].item
            tags_menu = page_menu.find_items(SubMenu, name=force_str(PAGE_TAGS_MENU_TITLE))[0].item
            self.assertEqual(
                len(tags_menu.find_items(ModalItem, name="{}...".format(force_str(PAGE_TAGS_ITEM_TITLE)))), 1
            )
            self.assertEqual(len(tags_menu.find_items(ModalItem)), len(NEW_CMS_LANGS[1]) + 1)

    def test_toolbar_with_items(self):
        """
        Test that PageTags/TitleTags items are present for superuser if PageTags/TitleTags exists for current page
        """
        from cms.toolbar.toolbar import CMSToolbar

        page1, page2 = self.get_pages()
        page_ext = PageTags.objects.create(extended_object=page1)
        title_tags = TitleTags.objects.create(extended_object=page1.get_title_obj("en"))
        request = self.get_page_request(page1, self.user, "/", edit=True)
        toolbar = CMSToolbar(request)
        toolbar.get_left_items()
        page_menu = toolbar.find_items(Menu, name="Page")[0].item
        tags_menu = page_menu.find_items(SubMenu, name=force_str(PAGE_TAGS_MENU_TITLE))[0].item
        pagetags_menu = tags_menu.find_items(ModalItem, name="{}...".format(force_str(PAGE_TAGS_ITEM_TITLE)))
        self.assertEqual(len(pagetags_menu), 1)
        self.assertEqual(len(pagetags_menu), 1)
        self.assertTrue(
            pagetags_menu[0].item.url.startswith(
                reverse("admin:djangocms_page_tags_pagetags_change", args=(page_ext.pk,))
            )
        )
        url_change = False
        url_add = False
        for title in page1.title_set.all():
            language = get_language_object(title.language)
            titletags_menu = tags_menu.find_items(ModalItem, name="{}...".format(language["name"]))
            self.assertEqual(len(titletags_menu), 1)
            try:
                title_ext = TitleTags.objects.get(extended_object_id=title.pk)
                self.assertEqual(title_ext, title_tags)
                self.assertTrue(
                    titletags_menu[0].item.url.startswith(
                        reverse("admin:djangocms_page_tags_titletags_change", args=(title_ext.pk,))
                    )
                )
                url_change = True
            except TitleTags.DoesNotExist:
                self.assertTrue(
                    titletags_menu[0].item.url.startswith(reverse("admin:djangocms_page_tags_titletags_add"))
                )
                url_add = True
        self.assertTrue(url_change and url_add)
