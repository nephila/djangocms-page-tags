from cms.utils.conf import get_cms_setting
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from djangocms_helper.utils import DJANGO_1_11

admin.autodiscover()

urlpatterns = [
    url(r"^taggit_autosuggest/", include("taggit_autosuggest.urls")),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),
    url(r"^media/cms/(?P<path>.*)$", serve, {"document_root": get_cms_setting("MEDIA_ROOT"), "show_indexes": True}),
]

urlpatterns += staticfiles_urlpatterns()

if not DJANGO_1_11:
    urlpatterns += i18n_patterns(
        url(r"^admin/", admin.site.urls),
        url(r"^", include("cms.urls")),
    )
else:
    urlpatterns += i18n_patterns(
        url(r"^admin/", include(admin.site.urls)),
        url(r"^", include("cms.urls")),
    )
