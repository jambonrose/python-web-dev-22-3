"""Utility code for tests

I'm breaking the rules here for simplicity: this should not
be in config, as this is not configuration for the project.
However, introducing an app specifically for test utilities
would overcomplicate the work we're doing, so it's going
here instead.

"""
from contextlib import contextmanager
from functools import reduce
from operator import or_

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField
from django.test import RequestFactory
from rest_framework.reverse import reverse as rf_reverse

User = get_user_model()
USERNAME_FIELD = getattr(User, "USERNAME_FIELD", "username")


def lmap(*args, **kwargs):
    """Shortcut to return list when mapping"""
    return list(map(*args, **kwargs))


def omit_keys(*args):
    """Remove keys from a dictionary"""
    *keys, dict_obj = args
    return {
        field: value
        for field, value in dict_obj.items()
        if field not in keys
    }


def reverse(name, *args, **kwargs):
    """Shorter Reverse function for the very lazy tester"""
    full_url = kwargs.pop("full", False)
    uri = rf_reverse(name, args=args, kwargs=kwargs)
    if "request" not in kwargs and full_url:
        return f"http://testserver{uri}"
    return uri


def context_kwarg(path):
    """Build context for Serializers

    Not necessary from the outset, but the use of
    Hyperlinked fields and serializers necessitates the
    inclusion of a request. This utility is pre-empting
    that requirement.
    """
    return {
        "context": {"request": RequestFactory().get(path)}
    }


@contextmanager
def auth_user(testcase):
    """Create new user and log them in

    permissions should be a string identifying a permission,
    e.g. contenttypes.add_contenttype or contenttypes.*
    or else a list of such strings
    """
    password = getattr(
        testcase, "password", "securepassword!"
    )
    if (
        not hasattr(testcase, "user_factory")
        or testcase.user_factory is None
    ):
        raise ImproperlyConfigured(
            "Testcase must specify a user factory "
            "to use the perm_user context"
        )
    test_user = testcase.user_factory(password=password)
    credentials = {
        USERNAME_FIELD: getattr(test_user, USERNAME_FIELD),
        "password": password,
    }
    success = testcase.client.login(**credentials)
    testcase.assertTrue(
        success,
        "login failed with credentials=%r" % (credentials),
    )
    yield test_user
    testcase.client.logout()


def get_perms(string_perm):
    """Build Q() of permission identified by string_perm

    expects: contenttypes.add_contenttype or contenttypes.*
    """
    if "." not in string_perm:
        raise ImproperlyConfigured(
            "The permission in the perms argument needs to be either "
            "app_label.codename or app_label.* "
            "(e.g. contenttypes.add_contenttype or contenttypes.*)"
        )
    app_label, codename = string_perm.split(".")
    if codename == "*":
        return Q(content_type__app_label=app_label)
    else:
        return Q(
            content_type__app_label=app_label,
            codename=codename,
        )


@contextmanager
def perm_user(testcase, permissions):
    """Create new user with permissions and log them in

    permissions should be a string identifying a permission,
    e.g. contenttypes.add_contenttype or contenttypes.*
    or else a list of such strings
    """
    with auth_user(testcase) as test_user:
        if isinstance(permissions, str):
            test_user.user_permissions.add(
                *list(
                    Permission.objects.filter(
                        get_perms(permissions)
                    )
                )
            )
        else:
            test_user.user_permissions.add(
                *list(
                    Permission.objects.filter(
                        reduce(
                            or_,
                            (
                                get_perms(perms)
                                for perms in permissions
                            ),
                        )
                    )
                )
            )
        yield test_user


def get_concrete_field_names(Model):
    """Return all of the concrete field names for a Model

    https://docs.djangoproject.com/en/2.2/ref/models/meta/

    """
    return [
        field.name
        for field in Model._meta.get_fields()
        if field.concrete
        and (
            not (
                field.is_relation
                or field.one_to_one
                or (
                    field.many_to_one
                    and field.related_model
                )
            )
        )
    ]


def get_instance_data(model_instance, related_value="pk"):
    """Return a dict of fields for the model_instance instance

    Effectively a simple form of serialization

    """
    from django.db.models import DateField, DateTimeField

    model_fields = model_instance._meta.get_fields()

    # add basic fields
    concrete_fields = [
        field
        for field in model_fields
        if field.concrete
        and not isinstance(
            field, (DateField, DateTimeField)
        )
    ]
    instance_data = {
        field.name: field.value_from_object(model_instance)
        for field in concrete_fields
        if field.value_from_object(model_instance)
        is not None
    }

    # special case for datefields to ensure a string, not an object
    concrete_date_fields = [
        field
        for field in model_fields
        if field.concrete
        and isinstance(field, (DateField, DateTimeField))
    ]
    for field in concrete_date_fields:
        instance_data[field.name] = str(
            field.value_from_object(model_instance)
        )

    # add many-to-many fields
    # the `isinstance` check avoids ManyToManyRel
    m2m_fields = [
        field
        for field in model_fields
        if field.many_to_many
        and isinstance(field, ManyToManyField)
    ]
    if model_instance.pk is None:
        for field in m2m_fields:
            instance_data[field.name] = []
    else:
        for field in m2m_fields:
            instance_data[field.name] = [
                getattr(obj, related_value)
                for obj in field.value_from_object(
                    model_instance
                )
            ]

    return instance_data
