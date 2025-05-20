from rest_framework import status
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from domain.user.selectors import user_get
from domain.user.serializers import UserOutputSerializer
from domain.user.actions import user_update
from drf_spectacular.utils import extend_schema 

@extend_schema(
    summary="Remove um usuário",
    tags=["Usuários"],
    responses={200: UserOutputSerializer, 404: {"detail": "User not found"}}
)
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_delete_api(request, pk):
    if not request.user.has_perm("user.delete_user"):
        raise PermissionDenied

    user = user_get(user_id=pk)
    if not user:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    user_update(user=user, data={"is_active": False})

    serializer = UserOutputSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
