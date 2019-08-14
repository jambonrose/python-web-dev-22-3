"""URL Configuration for User management

https://docs.djangoproject.com/en/2.2/topics/auth/default/#using-the-views
https://github.com/django/django/blob/stable/2.2.x/django/contrib/auth/urls.py
https://ccbv.co.uk/projects/Django/2.2/
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from .views import PasswordChangeView

urlpatterns = [
    path(
        "account/",
        login_required(
            TemplateView.as_view(
                template_name="user/account.html"
            )
        ),
        name="account",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
]
