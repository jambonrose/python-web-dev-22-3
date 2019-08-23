"""Generate feeds to blog posts"""
from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.feedgenerator import (
    Atom1Feed,
    Rss201rev2Feed,
)

from .models import Post


class BasePostFeedMixin:
    """Base class for Atom/RSS feeds"""

    title = "Latest Startup Organizer Blog Posts"
    link = reverse_lazy("post_list")
    description = subtitle = (
        "Stay up to date on the " "hottest startup news."
    )

    def items(self):
        """List of items in the feed"""
        # uses Post.Meta.ordering
        return Post.objects.all()[:10]

    def item_title(self, item):
        """Feed item title for each item"""
        return item.title.title()

    def item_description(self, item):
        """Content of the feeed item"""
        return item.short_text()

    def item_link(self, item):
        """Link to the actual content"""
        return item.get_absolute_url()


class AtomPostFeed(BasePostFeedMixin, Feed):
    """Feed for Atom syndication format"""

    feed_type = Atom1Feed


class Rss2PostFeed(BasePostFeedMixin, Feed):
    """Feed for RSS (Rich Site Summary) format"""

    feed_type = Rss201rev2Feed
