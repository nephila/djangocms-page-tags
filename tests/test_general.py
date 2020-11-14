from django.core.cache import cache
from django.template.defaultfilters import slugify
from taggit.models import Tag

from djangocms_page_tags import models
from djangocms_page_tags.utils import (
    get_cache_key,
    get_page_tags,
    get_page_tags_from_request,
    get_title_tags,
    get_title_tags_from_request,
    page_has_tag,
    title_has_tag,
)

from . import BaseTest


class PageTagsUtilsTest(BaseTest):
    tag_strings = ["tag one", "tag two", "tag three"]
    tag_strings_fr = ["tag un", "tag deux", "tag trois"]
    tag_strings_it = ["tag uno", "tag due", "tag tre"]

    def test_page_tags(self):
        """
        Tests the correct retrieval of tags for a page
        """
        page, page_2 = self.get_pages()
        page_tags = models.PageTags.objects.create(extended_object=page)
        page_tags.tags.add(*self.tag_strings)

        self.assertTrue(page_has_tag(page, slugify(self.tag_strings[0])))
        self.assertTrue(page_has_tag(page, Tag.objects.get(slug=slugify(self.tag_strings[0]))))
        self.assertEqual(set(self.tag_strings), {tag.name for tag in get_page_tags(page)})

        self.assertFalse(page_has_tag(page_2, slugify(self.tag_strings[0])))
        self.assertEqual(set(), {tag.name for tag in get_page_tags(page_2)})

    def test_title_tags(self):
        """
        Tests the correct retrieval of tags for a title
        """
        page, page_2 = self.get_pages()

        # Assign and test english tags
        title_en = page.get_title_obj(language="en")
        title_en_tags = models.TitleTags.objects.create(extended_object=title_en)
        title_en_tags.tags.add(*self.tag_strings)

        self.assertTrue(title_has_tag(page, "en", slugify(self.tag_strings[0])))
        self.assertTrue(title_has_tag(page, "en", Tag.objects.get(slug=slugify(self.tag_strings[0]))))
        self.assertEqual(set(self.tag_strings), {tag.name for tag in get_title_tags(page, "en")})

        # Assign and test french tags
        title_fr = page.get_title_obj(language="fr", fallback=False)
        title_fr_tags = models.TitleTags.objects.create(extended_object=title_fr)
        title_fr_tags.tags.add(*self.tag_strings_fr)
        self.assertTrue(title_has_tag(page, "fr", slugify(self.tag_strings_fr[0])))
        self.assertEqual(set(self.tag_strings_fr), {tag.name for tag in get_title_tags(page, "fr")})

        self.assertFalse(title_has_tag(page, "it", slugify(self.tag_strings_fr[0])))
        self.assertEqual(set(), {tag.name for tag in get_title_tags(page, "it")})

    def test_tags_request_page(self):
        """
        Tests the correct retrieval of tags for a page  from request
        """
        page, page_2 = self.get_pages()

        # Assign tags to page
        page_tags = models.PageTags.objects.create(extended_object=page)
        page_tags.tags.add(*self.tag_strings)
        for lang in self.languages:
            page.publish(lang)

        cache.clear()
        # Reload page from request and extract tags from it
        request = self.get_request(page, "en")
        site_id = page.node.site_id

        with self.assertNumQueries(4):
            # 1st query to get the page for the key lookup
            # 2st query to get the page in get_page_tags_from_request
            # 3nd query to get the page extension
            # 4rd query to extract tags data
            tags_list = get_page_tags_from_request(request, page.get_public_object().pk, "en", site_id)
        self.assertEqual(set(self.tag_strings), {tag.name for tag in tags_list})

        with self.assertNumQueries(1):
            # Second run executes exactly 1 query as data is fetched from cache
            # 1st query to get the page for the key lookup
            tags_list = get_page_tags_from_request(request, page.get_public_object().pk, "en", site_id)

        # Empty page has no tags
        tags_list = get_page_tags_from_request(request, 40, "en", 1)
        self.assertEqual(set(), set(tags_list))

    def test_tags_request_title(self):
        """
        Tests the correct retrieval of tags for a title from request
        """
        page, page_2 = self.get_pages()

        # Assign tags to title
        title_tags = models.TitleTags.objects.create(extended_object=page.get_title_obj("en"))
        title_tags.tags.add(*self.tag_strings)
        for lang in self.languages:
            page.publish(lang)

        site_id = page.node.site_id

        # Reload page from request and extract tags from it
        request = self.get_request(page, "en")
        tags_list = get_title_tags_from_request(request, page.get_public_object().pk, "en", site_id)
        self.assertEqual(set(self.tag_strings), {tag.name for tag in tags_list})

    def test_cache_cleanup(self):
        """
        Tests the correct retrieval of tags for a title from request
        """
        page, page_2 = self.get_pages()

        # Assign tags to title
        title_tags = models.TitleTags.objects.create(extended_object=page.get_title_obj("en"))
        title_tags.tags.add(*self.tag_strings)
        page_tags = models.PageTags.objects.create(extended_object=page)
        page_tags.tags.add(*self.tag_strings)
        for lang in self.languages:
            page.publish(lang)

        site_id = page.node.site_id

        # Reload page from request and extract tags from it
        request = self.get_request(page, "en")
        title_tags_list = get_title_tags_from_request(request, page.get_public_object().pk, "en", site_id)
        page_tags_list = get_page_tags_from_request(request, page.get_public_object().pk, "en", site_id)

        try:
            site_id = page.get_public_object().node.site_id
        except AttributeError:  # CMS_3_4
            site_id = page.get_public_object().site_id
        title_key = get_cache_key(None, page.get_public_object(), "en", site_id, True)
        page_key = get_cache_key(None, page.get_public_object(), "", site_id, False)

        title_cache = cache.get(title_key)
        page_cache = cache.get(page_key)

        self.assertEqual(set(title_tags_list), set(title_cache))
        self.assertEqual(set(page_tags_list), set(page_cache))

        page.get_public_object().get_title_obj("en").delete()
        self.assertIsNone(cache.get(title_key))

        page.get_public_object().delete()
        self.assertIsNone(cache.get(page_key))
