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


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail_api(request, pk):
    if not request.user.has_perm("user.view_user"):
        raise PermissionDenied
    user = user_get(user_id=pk)

    serializer = UserOutputSerializer(user)

    return Response(status=status.HTTP_200_OK, data=serializer.data)
