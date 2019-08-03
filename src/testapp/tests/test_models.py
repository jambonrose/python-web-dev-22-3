"""Model tests for testapp"""
from django.db import IntegrityError
from django.test import TestCase

from ..models import Tag
from .factories import TagFactory


class TagModelTestDemo(TestCase):
    """Tests for the Tag model"""

    def test_concrete_fields(self):
        """Does Tag have the fields we expect?

        https://docs.djangoproject.com/en/2.2/ref/models/meta/
        """
        field_names = [
            field.name for field in Tag._meta.get_fields()
        ]
        expected_field_names = ["id", "name", "slug"]
        self.assertEqual(field_names, expected_field_names)

    def test_name_uniqueness(self):
        """Are Tags with identical names disallowed?"""
        kwargs = dict(name="a")
        TagFactory(**kwargs)
        with self.assertRaises(IntegrityError):
            TagFactory(**kwargs)

    def test_list_order(self):
        """Are tags ordered by name?

        This test is actually dependent on the database and whether the
        field is unique. In SQLite3, the order will be alphabetical if
        the name field is unique.

        Will pass regardless if/once Meta ordering is defined.

        """
        TagFactory(name="b")
        TagFactory(name="D")
        TagFactory(name="c")
        TagFactory(name="a")
        tag_name_list = list(
            Tag.objects.values_list("name", flat=True)
        )
        expected_name_list = ["D", "a", "b", "c"]
        self.assertEqual(tag_name_list, expected_name_list)

    def test_str(self):
        """Do Tags clearly represent themselves?"""
        t = TagFactory(name="django")
        self.assertEqual(str(t), "django")
