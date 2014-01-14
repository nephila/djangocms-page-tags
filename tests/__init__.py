# -*- coding: utf-8 -*-
"""
Tests for `djangocms_page_tags` module.
"""

from django.contrib.auth.models import User
from django.http import SimpleCookie
from django.test import TestCase, RequestFactory
from six import StringIO
from cms.models import Page
from djangocms_page_tags.models import TitleTags, PageTags


class BaseTest(TestCase):
    """
    Base class with utility function
    """
    request_factory = None
    user = None

    @classmethod
    def setUpClass(cls):
        cls.request_factory = RequestFactory()
        cls.user = User.objects.create(username='admin', is_staff=True, is_superuser=True)
        cls.user_staff = User.objects.create(username='staff', is_staff=True)
        cls.user_normal = User.objects.create(username='normal')

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

    def get_page_request(self, page, user, path=None, edit=False, lang_code='en'):
        from cms.middleware.toolbar import ToolbarMiddleware
        path = path or page and page.get_absolute_url()
        if edit:
            path += '?edit'
        request = RequestFactory().get(path)
        request.session = {}
        request.user = user
        request.LANGUAGE_CODE = lang_code
        if edit:
            request.GET = {'edit': None}
        else:
            request.GET = {'edit_off': None}
        request.current_page = page
        mid = ToolbarMiddleware()
        mid.process_request(request)
        return request

    def tearDown(self):
        Page.objects.all().delete()
        PageTags.objects.all().delete()
        TitleTags.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
