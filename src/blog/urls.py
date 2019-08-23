"""URL paths for Blog App"""
from django.urls import path

from .views import (
    PostArchiveMonth,
    PostArchiveYear,
    PostCreate,
    PostDelete,
    PostDetail,
    PostList,
    PostUpdate,
)

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path(
        "create/", PostCreate.as_view(), name="post_create"
    ),
    path(
        "<int:year>/",
        PostArchiveYear.as_view(),
        name="post_archive_year",
    ),
    path(
        "<int:year>/<int:month>/",
        PostArchiveMonth.as_view(),
        name="post_archive_month",
    ),
    path(
        "<int:year>/<int:month>/<str:slug>/",
        PostDetail.as_view(),
        name="post_detail",
    ),
    path(
        "<int:year>/<int:month>/<str:slug>/delete/",
        PostDelete.as_view(),
        name="post_delete",
    ),
    path(
        "<int:year>/<int:month>/<str:slug>/update/",
        PostUpdate.as_view(),
        name="post_update",
    ),
]
