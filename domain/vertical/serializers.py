from rest_framework import serializers
from domain.user.serializers import UserOutputSerializer
from domain.vertical.models import Vertical, PlanVertical
from domain.plan.serializers import PlanSerializer

class VerticalOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, min_length=2)
    created_by = UserOutputSerializer(required=False)
    updated_by = UserOutputSerializer(required=False)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

class CreateVerticalSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2)
    
class PlanVerticalOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    plan = PlanSerializer(required=True)
    vertical = VerticalOutputSerializer(required=True)
    created_by = UserOutputSerializer(required=False)
    updated_by = UserOutputSerializer(required=False)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

class CreatePlanVerticalSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField(required=True)
    vertical_id = serializers.IntegerField(required=True)
