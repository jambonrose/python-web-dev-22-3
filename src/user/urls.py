"""URL Configuration for User management

https://docs.djangoproject.com/en/2.2/topics/auth/default/#using-the-views
https://github.com/django/django/blob/stable/2.2.x/django/contrib/auth/urls.py
https://ccbv.co.uk/projects/Django/2.2/

https://django-registration.readthedocs.io/en/3.0.1/activation-workflow.html
https://django-registration.readthedocs.io/en/3.0.1/custom-user.html
https://github.com/ubernostrum/django-registration/blob/58be01f5858a95d30f99eb618d15363323c5d168/src/django_registration/backends/activation/urls.py#L13
"""
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path, reverse_lazy
from django.views.generic import TemplateView
from django_registration.backends.activation.views import (
    ActivationView,
    RegistrationView,
)

from .forms import RegistrationForm
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
    path(
        "activate/complete/",
        TemplateView.as_view(
            template_name="django_registration/activation_complete.html"
        ),
        name="django_registration_activation_complete",
    ),
    re_path(
        r"^activate/(?P<activation_key>[-:\w]+)/$",
        ActivationView.as_view(
            success_url=reverse_lazy(
                "auth:django_registration_activation_complete"
            )
        ),
        name="django_registration_activate",
    ),
    path(
        "register/",
        RegistrationView.as_view(
            form_class=RegistrationForm,
            success_url=reverse_lazy(
                "auth:django_registration_complete"
            ),
        ),
        name="django_registration_register",
    ),
    path(
        "register/complete/",
        TemplateView.as_view(
            template_name="django_registration/registration_complete.html"
        ),
        name="django_registration_complete",
    ),
    path(
        "register/closed/",
        TemplateView.as_view(
            template_name="django_registration/registration_closed.html"
        ),
        name="django_registration_disallowed",
    ),
]
