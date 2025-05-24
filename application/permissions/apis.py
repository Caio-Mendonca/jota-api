from django.core.exceptions import PermissionDenied

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from application.authentication.mixins import (
    JWTAuthentication,
)

from .selectors import group_list

class OutputSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return dict({"value": instance.id, "label": instance.name})

@extend_schema(
    summary="Grupos",
    tags=["Grupos"],
    responses={200: None},
)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def group_list_api(request):
    if not request.user.has_perm("auth.view_group"):
        raise PermissionDenied

    groups = group_list()

    serializer = OutputSerializer(groups, many=True)

    return Response(status=status.HTTP_200_OK, data={"groups": serializer.data})
