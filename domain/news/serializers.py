from rest_framework import serializers
from domain.user.models import User
from domain.user.serializers import UserOutputSerializer
from domain.news.models import NewsStatus
from domain.file.models import File
from domain.vertical.models import Vertical


class OutputNewsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, min_length=2)
    subtitle = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    content = serializers.CharField(required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), required=False, allow_null=True)
    author = UserOutputSerializer(required=True)
    publication_date = serializers.DateTimeField(required=False, allow_null=True)
    status = serializers.ChoiceField(choices=NewsStatus.choices, required=True)
    access_pro = serializers.BooleanField(default=False)
    vertical = serializers.PrimaryKeyRelatedField(queryset=Vertical.objects.all())
    created_by = UserOutputSerializer(required=False)
    updated_by = UserOutputSerializer(required=False)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)


class CreateNewsSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2)
    subtitle = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    content = serializers.CharField(required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), required=False, allow_null=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    publication_date = serializers.DateTimeField(required=False, allow_null=True)
    status = serializers.ChoiceField(choices=NewsStatus.choices, required=False, default=NewsStatus.DRAFT)
    access_pro = serializers.BooleanField(required=False, default=False)
    vertical = serializers.PrimaryKeyRelatedField(queryset=Vertical.objects.all())


class NewsUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2)
    subtitle = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    content = serializers.CharField(required=True)
    image = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), required=False, allow_null=True)
    publication_date = serializers.DateTimeField(required=False, allow_null=True)
    status = serializers.ChoiceField(choices=NewsStatus.choices, required=False)
    access_pro = serializers.BooleanField(required=False)
    vertical = serializers.PrimaryKeyRelatedField(queryset=Vertical.objects.all(), required=False)
