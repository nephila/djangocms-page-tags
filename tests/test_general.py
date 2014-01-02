# -*- coding: utf-8 -*-
"""
test_djangocms_page_tags
------------

Tests for `djangocms_page_tags` modules module.
"""
from cms.models import Page
from django.contrib.auth.models import User
from django.http import SimpleCookie
from django.test import TestCase, RequestFactory
from django.template.defaultfilters import slugify
from six import StringIO
from taggit.models import Tag

from djangocms_page_tags import models
from djangocms_page_tags.utils import (page_has_tag, get_page_tags,
                                       title_has_tag, get_title_tags,
                                       get_page_tags_from_request,
                                       get_title_tags_from_request)


class TestPageTagsUtils(TestCase):
    request_factory = None
    user = None
    tag_strings = [u"tag one", u"tag two", u"tag three"]
    tag_strings_fr = [u"tag un", u"tag deux", u"tag trois"]
    tag_strings_it = [u"tag uno", u"tag due", u"tag tre"]

    @classmethod
    def setUpClass(cls):
        cls.request_factory = RequestFactory()
        cls.user = User.objects.create(username='admin', is_staff=True)

    def get_pages(self):
        from cms.api import create_page, create_title
        page = create_page(u'page one', 'page.html', language='en')
        page_2 = create_page(u'page two', 'page.html', language='en')
        create_title(language='fr', title=u'page un', page=page)
        create_title(language='it', title=u'pagina uno', page=page)
        page.publish()
        page_2.publish()
        return page.get_draft_object(), page_2.get_draft_object()

    def get_request(self, page, lang):
        request = self.request_factory.get(page.get_path(lang))
        request.current_page = page
        request.user = self.user
        request.session = {}
        request.cookies = SimpleCookie()
        request.errors = StringIO()
        return request

    def test_page_tags(self):
        """
        Tests the correct retrieval of tags for a page
        """
        page, page_2 = self.get_pages()
        page_tags = models.PageTags.objects.create(extended_object=page)
        page_tags.tags.add(*self.tag_strings)

        self.assertTrue(page_has_tag(page, slugify(self.tag_strings[0])))
        self.assertTrue(page_has_tag(page, Tag.objects.get(slug=slugify(self.tag_strings[0]))))
        self.assertEqual(set(self.tag_strings), set([tag.name for tag in get_page_tags(page)]))

        self.assertFalse(page_has_tag(page_2, slugify(self.tag_strings[0])))
        self.assertEqual(set(), set([tag.name for tag in get_page_tags(page_2)]))

    def test_title_tags(self):
        """
        Tests the correct retrieval of tags for a title
        """
        page, page_2 = self.get_pages()

        # Assign and test english tags
        title_en = page.get_title_obj(language='en')
        title_en_tags = models.TitleTags.objects.create(extended_object=title_en)
        title_en_tags.tags.add(*self.tag_strings)

        self.assertTrue(title_has_tag(page, 'en', slugify(self.tag_strings[0])))
        self.assertTrue(title_has_tag(page, 'en', Tag.objects.get(slug=slugify(self.tag_strings[0]))))
        self.assertEqual(set(self.tag_strings), set([tag.name for tag in get_title_tags(page, 'en')]))

        # Assign and test french tags
        title_fr = page.get_title_obj(language='fr', fallback=False)
        title_fr_tags = models.TitleTags.objects.create(extended_object=title_fr)
        title_fr_tags.tags.add(*self.tag_strings_fr)
        self.assertTrue(title_has_tag(page, 'fr', slugify(self.tag_strings_fr[0])))
        self.assertEqual(set(self.tag_strings_fr), set([tag.name for tag in get_title_tags(page, 'fr')]))

        self.assertFalse(title_has_tag(page, 'it', slugify(self.tag_strings_fr[0])))
        self.assertEqual(set(), set([tag.name for tag in get_title_tags(page, 'it')]))

    def test_tags_request_page(self):
        """
        Tests the correct retrieval of tags for a page  from request
        """
        page, page_2 = self.get_pages()

        # Assign tags to page
        page_tags = models.PageTags.objects.create(extended_object=page)
        page_tags.tags.add(*self.tag_strings)
        page.publish()


        # Reload page from request and extract tags from it
        request = self.get_request(page, 'en')
        with self.assertNumQueries(3):
            # 1st query to get the page
            # 2nd query to get the page extension
            # 3rd query to extract tags data
            tags_list = get_page_tags_from_request(request, page.get_public_object().pk, 'en', None)
        self.assertEqual(set(self.tag_strings), set([tag.name for tag in tags_list]))

        with self.assertNumQueries(0):
            # Second run executes exactly zero queries as data is fetched from cache
            tags_list = get_page_tags_from_request(request, page.get_public_object().pk, 'en', None)

        # Empty page has no tags
        tags_list = get_page_tags_from_request(request, 40, 'en', None)
        self.assertEqual(set(), set(tags_list))

    def test_tags_request_title(self):
        """
        Tests the correct retrieval of tags for a title from request
        """
        page, page_2 = self.get_pages()

        # Assign tags to title
        title_tags = models.TitleTags.objects.create(extended_object=page.get_title_obj('en'))
        title_tags.tags.add(*self.tag_strings)
        page.publish()

        # Reload page from request and extract tags from it
        request = self.get_request(page, 'en')
        tags_list = get_title_tags_from_request(request, page.get_public_object().pk, None, None)
        self.assertEqual(set(self.tag_strings), set([tag.name for tag in tags_list]))

    def tearDown(self):
        pass