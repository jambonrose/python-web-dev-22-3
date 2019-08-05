"""Signals for User authentication"""
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
)
from django.contrib.messages import success
from django.dispatch import receiver


@receiver(user_logged_in)
def display_login_message(sender, **kwargs):
    """Inform user they've successfully logged in"""
    request = kwargs.get("request")
    user = kwargs.get("user")
    name = user.get_short_name()
    success(
        request,
        f"Successfully logged in as {name}",
        fail_silently=True,
    )


@receiver(user_logged_out)
def display_logout_message(sender, **kwargs):
    """Inform user they've successfully logged out"""
    request = kwargs.get("request")
    success(
        request,
        "Successfully logged out",
        fail_silently=True,
    )
