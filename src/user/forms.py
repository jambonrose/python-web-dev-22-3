"""Forms for user app

https://django-registration.readthedocs.io/en/3.0.1/custom-user.html#the-two-step-activation-workflow
"The username and email fields must be distinct."

https://github.com/ubernostrum/django-registration/blob/58be01f5858a95d30f99eb618d15363323c5d168/src/django_registration/forms.py#L23
https://github.com/django/django/blob/6624a3de286ccebf2dafba5a3e9b5ee91ae43cf9/django/contrib/auth/forms.py#L65
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django_registration.validators import (
    DUPLICATE_EMAIL,
    CaseInsensitiveUnique,
    validate_confusables_email,
)

User = get_user_model()


class RegistrationForm(UserCreationForm):
    """Form for registering a new user account.

    Validates that the requested email is not already in use, and
    requires the password to be entered twice to catch typos.
    """

    class Meta:
        model = User
        fields = [
            User.USERNAME_FIELD,
            "password1",
            "password2",
            "full_name",
            "short_name",
        ]
        field_classes = {}

    error_css_class = "error"
    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        """Configure username/email field to be validated"""
        super().__init__(*args, **kwargs)
        self.fields[User.USERNAME_FIELD].validators.extend(
            [
                validate_confusables_email,
                CaseInsensitiveUnique(
                    User,
                    User.USERNAME_FIELD,
                    DUPLICATE_EMAIL,
                ),
            ]
        )
