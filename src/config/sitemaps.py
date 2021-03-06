"""Configure sitemaps for entire site"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.sitemaps import PostArchiveSitemap, PostSitemap
from organizer.sitemaps import StartupSitemap, TagSitemap


class RootSitemap(Sitemap):
    """Generate sitemap for pages not generated by DB"""

    priority = 0.6

    def items(self):
        """URL path names to include in sitemap"""
        return [
            "post_list",
            "auth:login",
            "startup_list",
            "tag_list",
        ]

    def location(self, url_name):
        """Reverse location of URL paths"""
        return reverse(url_name)


sitemaps = {
    "post-archives": PostArchiveSitemap,
    "posts": PostSitemap,
    "roots": RootSitemap,
    "startups": StartupSitemap,
    "tags": TagSitemap,
}
