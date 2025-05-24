from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from domain.file.serializers import FileOutputSerializer
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
    summary="Detalhe sobre um arquivo",
    tags=["Arquivos"],
    responses={200: FileOutputSerializer, 404: {"detail": "Arquivo não encontrado"}},
)
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def file_detail_api(request, pk):
    if not request.user.has_perm("file.view_file"):
        raise PermissionDenied
    file = file_get(file_id=pk)

    serializer = FileOutputSerializer(file)

    return Response(status=status.HTTP_200_OK, data=serializer.data)