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
from domain.user.serializers import InputSerializer
from domain.user.actions import user_create


@extend_schema(
    summary="Cria um novo usuário",
    tags=["Usuários"],
    request=InputSerializer,
    responses={201: None},
)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_create_api(request):
    if not request.user.has_perm("user.add_user"):
        raise PermissionDenied
    serializer = InputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_create(**serializer.validated_data)

    return Response(status=status.HTTP_201_CREATED)
