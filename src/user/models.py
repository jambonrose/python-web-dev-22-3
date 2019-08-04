"""User model for site

Future-proofs application against migration issues in the event of User model
changes.

https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
"""
from improved_user.model_mixins import AbstractUser


class User(AbstractUser):
    """A User model that extends the Improved User

    https://django-improved-user.readthedocs.io/en/latest/quickstart.html
    """

    def __str__(self):
        return self.email
