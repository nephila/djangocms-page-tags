# -*- coding: utf-8 -*-
from cms.views import details
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _
from taggit.models import Tag

from djangocms_page_tags.models import PageTags, TitleTags
from tests import BaseTest


class TemplateTagsTest(BaseTest):

    def test_page_tags(self):
        """
        Test page-level templatetags
        """
        page1, page2 = self.get_pages()
        page_ext = PageTags.objects.create(extended_object=page1)
        page_ext.tags.add("pagetag.1", "pagetag.2")
        for lang in self.languages:
            page1.publish(lang)
        tags = Tag.objects.filter(name__in=("pagetag.1", "pagetag.2"))

        request = self.get_page_request(page1.get_public_object(), AnonymousUser())
        response = details(request, '')
        self.assertContains(response, '<ul><li>pagetag.1</li><li>pagetag.2</li></ul>')
        self.assertEqual(set(response.context_data['ptags_list']), set(tags))
        self.assertEqual(set(response.context_data['ttags_list']), set())

    def test_title_tags(self):
        """
        Test title-level templatetags
        """
        page1, page2 = self.get_pages()
        title_ext = TitleTags.objects.create(extended_object=page1.get_title_obj('en'))
        title_ext.tags.add("titletag.1", "titletag.2")
        for lang in self.languages:
            page1.publish(lang)
        tags = Tag.objects.filter(name__in=("titletag.1", "titletag.2"))

        request = self.get_page_request(page1.get_public_object(), AnonymousUser())
        response = details(request, '')
        response.render()
        self.assertContains(response, '<ul><li>titletag.2</li><li>titletag.1</li></ul>')
        self.assertEqual(set(response.context_data['ttags_list']), set(tags))
        self.assertEqual(set(response.context_data['ptags_list']), set())
