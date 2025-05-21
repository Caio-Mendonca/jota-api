from rest_framework import serializers

from .models import File


class FileOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    path = serializers.FileField()
    type_file = serializers.ChoiceField(choices=File.TypeFile)