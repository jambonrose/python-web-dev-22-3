"""URL Configuration for User management

https://docs.djangoproject.com/en/2.2/topics/auth/default/#using-the-views
https://github.com/django/django/blob/stable/2.2.x/django/contrib/auth/urls.py
https://ccbv.co.uk/projects/Django/2.2/
"""
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    AccountPage,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)

urlpatterns = [
    path("account/", AccountPage.as_view(), name="account"),
    path(
        "login/",
        LoginView.as_view(template_name="user/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            template_name="user/logout.html"
        ),
        name="logout",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
