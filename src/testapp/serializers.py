"""Serializers for the Testapp"""
from rest_framework.serializers import ModelSerializer

from .models import Tag


class TagSerializer(ModelSerializer):
    """Serialize Tag data"""

    class Meta:
        model = Tag
        fields = "__all__"
