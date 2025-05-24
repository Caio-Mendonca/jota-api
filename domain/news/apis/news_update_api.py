from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from django.core.exceptions import PermissionDenied
from domain.news.serializers import CreateNewsSerializer, NewsUpdateSerializer, OutputNewsSerializer
from domain.news.actions import news_create, news_update


@extend_schema(
    summary="Atualiza uma notícia",
    tags=["Notícias"],
    request=NewsUpdateSerializer,
    responses={200: OutputNewsSerializer, 403:PermissionDenied},
)

@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def news_update_api(request):
    if not request.user.has_perm("news.change_news"):
        raise PermissionDenied
    serializer = NewsUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    news_update(**serializer.validated_data, created_by=request.user)
    serializer = OutputNewsSerializer(data=serializer.validated_data)
    
    return Response(status=status.HTTP_200_OK, data=serializer.data)
