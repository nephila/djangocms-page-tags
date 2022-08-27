from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    path("taggit_autosuggest", include("taggit_autosuggest.urls")),
    path("media/<str:path>", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),
]

urlpatterns += staticfiles_urlpatterns()

urlpatterns += i18n_patterns(
    path("admin", admin.site.urls),
    path("", include("cms.urls")),
)
