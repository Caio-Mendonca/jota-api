from rest_framework import serializers, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import Group
from domain.user.actions import user_update
from domain.user.selectors import user_get
from domain.user.serializers import InputUpdateSerializer, UserOutputSerializer
from drf_spectacular.utils import extend_schema
@extend_schema(
    summary="Atualiza um usuário",
    request=InputUpdateSerializer,
    tags=["Usuários"],
    responses={200: UserOutputSerializer},
)


@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_update_api(request, pk):
    if not request.user.has_perm("user.change_user"):
        raise PermissionDenied

    user = user_get(user_id=pk)

    serializer = InputUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = user_update(user=user, data=serializer.validated_data)

    serializer = UserOutputSerializer(user)

    return Response(status=status.HTTP_200_OK, data=serializer.data)
