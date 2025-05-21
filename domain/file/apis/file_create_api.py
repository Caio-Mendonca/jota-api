from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from domain.file.actions import file_create
from domain.file.models import File


@extend_schema(
    summary="Criar um novo arquivo",
    tags=["Arquivos"],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string', 'format': 'binary'},
                'type_file': {
                    'type': 'string',
                    'enum': [File.TypeFile.IMAGE, File.TypeFile.ATTACHMENT],
                    'description': 'Tipo do arquivo: "image" ou "attachment".'
                }
            },
            'required': ['path', 'type_file']
        }
    },
    responses={201: None},
)
class FileCreateApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm("file.add_file"):
            raise PermissionDenied

        uploaded_file = request.FILES.get('path')
        type_file = request.data.get('type_file')

        if not uploaded_file:
            return Response({'detail': 'Campo "path" (arquivo) é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        if not type_file:
            return Response({'detail': 'Campo "type_file" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        file = file_create(path=uploaded_file, type_file=type_file)

        return Response(status=status.HTTP_201_CREATED, data={"id": file.id})
