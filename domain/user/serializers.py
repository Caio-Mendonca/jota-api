from rest_framework import serializers
from django.contrib.auth.models import Group


class GroupField(serializers.RelatedField):
    def to_representation(self, value):
        return dict({"value": value.last().id, "label": value.last().name})


class UserOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    email = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    group = GroupField(read_only=True, source="groups")
    created_at = serializers.CharField(read_only=True)
    last_login = serializers.CharField(read_only=True)


class FilterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    ordering = serializers.CharField(required=False)
    search = serializers.CharField(required=False)


class InputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, min_length=2)
    password = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    group = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Group.objects.all()
    )

class InputUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    group = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Group.objects.all()
    )