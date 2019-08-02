"""Model tests for testapp"""
from django.test import TestCase

from ..models import Tag


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
