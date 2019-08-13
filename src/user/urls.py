"""URL Configuration for User management

https://docs.djangoproject.com/en/2.2/topics/auth/default/#using-the-views
https://github.com/django/django/blob/stable/2.2.x/django/contrib/auth/urls.py
https://ccbv.co.uk/projects/Django/2.2/
"""
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.urls import path, reverse_lazy

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            success_url=reverse_lazy(
                "auth:password_change_done"
            )
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
