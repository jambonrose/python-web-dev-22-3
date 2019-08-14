"""Views for User app"""
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
)
from django.contrib.messages import success
from django.urls import reverse_lazy


class SuccessMessageMixin:
    """Notify user of success after submitting a form"""

    success_message = "Success!"

    def form_valid(self, form):
        """When form is valid: notify user of success"""
        success(
            self.request,
            self.success_message,
            fail_silently=True,
        )
        return super().form_valid(form)


class PasswordChangeView(
    SuccessMessageMixin, BasePasswordChangeView
):
    """Allow authenticated users to change password;

    Messages success to user
    """

    success_message = "Password Changed Successfully"
    success_url = reverse_lazy("auth:account")
