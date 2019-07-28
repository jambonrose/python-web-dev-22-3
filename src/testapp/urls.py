"""URL paths for Test App"""
from django.urls import path

from .views import Status, pong

urlpatterns = [
    path("ping/", pong, name="ping"),
    path("status/", Status.as_view(), name="site_status"),
]
