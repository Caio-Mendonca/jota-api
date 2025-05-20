from rest_framework import serializers

from domain.user.serializers import UserOutputSerializer

class PlanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, min_length=2)
    description = serializers.CharField(required=False)
    created_by = UserOutputSerializer(required=False)
    updated_by = UserOutputSerializer(required=False)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)
    
class CreatePlanSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2)
    description = serializers.CharField(required=False)

class PlanUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2)
    description = serializers.CharField(required=False)