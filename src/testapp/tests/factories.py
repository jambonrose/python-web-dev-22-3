"""Factory classes for testapp"""
from factory import DjangoModelFactory, Sequence

from ..models import Tag


class TagFactory(DjangoModelFactory):
    """Factory for Tags (labels)"""

    name = Sequence(lambda n: f"name-{n}")

    class Meta:
        model = Tag
