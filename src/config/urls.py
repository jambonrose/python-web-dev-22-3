"""Root URL Configuration for Startup Organizer Project"""
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import (
    index as site_index_view,
    sitemap as sitemap_view,
)
from django.urls import include, path
from django.views.generic import TemplateView

from blog import urls as blog_urls
from blog.feeds import AtomPostFeed, Rss2PostFeed
from blog.routers import urlpatterns as blog_api_urls
from organizer import urls as organizer_urls
from organizer.routers import (
    urlpatterns as organizer_api_urls,
)
from user import urls as user_urls

from .sitemaps import sitemaps as sitemaps_dict
from .views import RootApiView, test_celery

root_api_url = [
    path("", RootApiView.as_view(), name="api-root")
]
api_urls = root_api_url + blog_api_urls + organizer_api_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_urls)),
    path("atom/", AtomPostFeed(), name="post_atom_feed"),
    path("blog/", include(blog_urls)),
    path(
        "o/",
        include(
            "oauth2_provider.urls",
            namespace="oauth2_provider",
        ),
    ),
    path("rss/", Rss2PostFeed(), name="post_rss_feed"),
    path(
        "sitemap.xml",
        site_index_view,
        {"sitemaps": sitemaps_dict},
        name="sitemap",
    ),
    path(
        "sitemap-<section>.xml",
        sitemap_view,
        {"sitemaps": sitemaps_dict},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("test/", test_celery),
    path("", include(organizer_urls)),
    path(
        "", include((user_urls, "auth"), namespace="auth")
    ),
    path(
        "",
        TemplateView.as_view(template_name="root.html"),
        name="site_root",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns
