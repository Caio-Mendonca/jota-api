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

from domain.plan.actions import plan_create, plan_update
from domain.plan.serializers import CreatePlanSerializer, PlanSerializer, PlanUpdateSerializer
from domain.user.selectors import user_get

@extend_schema(
    summary="Editar um plano",
    tags=["Planos"],
    request=CreatePlanSerializer,
    responses={201: None},
)
@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def plan_edit_api(request, pk):
    if not request.user.has_perm("plan.change_plan"):
        raise PermissionDenied
    user = user_get(user_id=pk)

    serializer = PlanUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    plan = plan_update()

    serializer = PlanSerializer(plan)

    return Response(status=status.HTTP_200_OK, data=serializer.data)