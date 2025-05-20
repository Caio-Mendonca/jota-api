from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from domain.plan.actions import plan_create
from domain.plan.serializers import CreatePlanSerializer

@extend_schema(
    summary="Cria um novo plano",
    tags=["Planos"],
    request=CreatePlanSerializer,
    responses={201: None},
)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def plan_create_api(request):
    if not request.user.has_perm("plan.add_plan"):
        raise PermissionDenied
    serializer = CreatePlanSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    plan_create(**serializer.validated_data)
    
    return Response(status=status.HTTP_201_CREATED)