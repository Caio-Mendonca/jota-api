from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from domain.file.selectors import file_get
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

@extend_schema(
    summary="Remove um arquivo",
    tags=["Arquivos"],
    responses={200},
)
@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def file_delete_api(request, pk):
    if not request.user.has_perm("file.delete_file"):
        raise PermissionDenied
    file = file_get(file_id=pk)
    file.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)