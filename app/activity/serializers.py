"""
Serilaizers for activity APIs.
"""
from rest_framework import serializers

from core.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """Serializers for activities."""

    class Meta:
        model = Activity
        fields = ['id', 'title', 'time_hours', 'price', 'link']
        read_only_fields = ['id']


class ActivityDetailSerializer(ActivitySerializer):
    """Serializer for activity detail view."""

    class Meta(ActivitySerializer.Meta):
        fields = ActivitySerializer.Meta.fields + ['description']
