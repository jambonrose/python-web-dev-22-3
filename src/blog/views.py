"""Views for Blog App

http://ccbv.co.uk/projects/Django/2.2/django.contrib.auth.mixins/PermissionRequiredMixin/
"""
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ArchiveIndexView,
    CreateView,
    DeleteView,
    DetailView,
    MonthArchiveView,
    UpdateView,
    YearArchiveView,
)

from .forms import PostForm
from .models import Post


class PostObjectMixin:
    """Django View mix-in to find blog posts"""

    model = Post

    def get_object(self, queryset=None):
        """Get a blog post using year, month, and slug

        http://ccbv.co.uk/SingleObjectMixin
        """
        if queryset is None:
            queryset = self.get_queryset()

        year, month, slug = map(
            self.kwargs.get, ["year", "month", "slug"]
        )
        if any(arg is None for arg in (year, month, slug)):
            raise AttributeError(
                f"View {self.__class__.__name__} must be"
                f"called with year, month, and slug for"
                f"Post objects"
            )
        return get_object_or_404(
            queryset,
            pub_date__year=year,
            pub_date__month=month,
            slug=slug,
        )


class PostArchiveMonth(MonthArchiveView):
    """Display blog posts for particular month

    http://ccbv.co.uk/projects/Django/2.2/django.views.generic.dates/MonthArchiveView/
    """

    date_field = "pub_date"
    model = Post
    month_format = "%m"
    template_name = "post/post_archive_month.html"


class PostArchiveYear(YearArchiveView):
    """Display blog posts for particular year

    http://ccbv.co.uk/projects/Django/2.2/django.views.generic.dates/YearArchiveView/
    """

    date_field = "pub_date"
    make_object_list = True
    model = Post
    template_name = "post/post_archive_year.html"


class PostCreate(PermissionRequiredMixin, CreateView):
    """Create new blog posts"""

    form_class = PostForm
    model = Post
    permission_required = "blog.add_post"
    template_name = "post/form.html"
    extra_context = {"update": False}


class PostDetail(PostObjectMixin, DetailView):
    """Display a single blog Post"""

    template_name = "post/detail.html"


class PostDelete(
    PermissionRequiredMixin, PostObjectMixin, DeleteView
):
    """Delete a single blog post"""

    permission_required = "blog.delete_post"
    template_name = "post/confirm_delete.html"
    success_url = reverse_lazy("post_list")


class PostList(ArchiveIndexView):
    """Display a list of blog Posts

    http://ccbv.co.uk/projects/Django/2.2/django.views.generic.dates/ArchiveIndexView/
    """

    allow_empty = True
    context_object_name = "post_list"
    date_field = "pub_date"
    make_object_list = True
    paginate_by = 5
    queryset = Post.objects.prefetch_related(
        "startups"
    ).prefetch_related("tags")
    template_name = "post/list.html"


class PostUpdate(
    PermissionRequiredMixin, PostObjectMixin, UpdateView
):
    """Update existing blog posts"""

    form_class = PostForm
    permission_required = "blog.change_post"
    template_name = "post/form.html"
    extra_context = {"update": True}
