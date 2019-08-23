"""Sitemaps for Tags and Startups"""
from django.contrib.sitemaps import GenericSitemap, Sitemap

from .models import Startup, Tag

TagSitemap = GenericSitemap({"queryset": Tag.objects.all()})


class StartupSitemap(Sitemap):
    """Sitemap for Startup pages"""

    def items(self):
        """All of our StartupSitemap

        Django uses get_absolute_url to generate links
        """
        return Startup.objects.all()

    def lastmod(self, startup):
        """Use Startup or Newslink to indicate when page was last modified"""
        if startup.newslink_set.exists():
            return startup.newslink_set.latest().pub_date
        else:
            return startup.founded_date
