from django.core.exceptions import PermissionDenied

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from domain.file.actions import file_update
from domain.file.serializers import FileOutputSerializer
from domain.file.selectors import file_get
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema


class InputSerializer(serializers.Serializer):
    path = serializers.FileField()


from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

@extend_schema(
    summary="Detalhe sobre um arquivo",
    request=InputSerializer,
    tags=["Arquivos"],
    responses={200: FileOutputSerializer, 404: {"detail": "Arquivo não encontrado"}},
)
@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def file_update_api(request, pk):
    if not request.user.has_perm("file.change_file"):
        raise PermissionDenied
    file = file_get(file_id=pk)

    serializer = InputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    file = file_update(file=file, data=serializer.validated_data)

    serializer = FileOutputSerializer(file)

    return Response(status=status.HTTP_200_OK, data=serializer.data)