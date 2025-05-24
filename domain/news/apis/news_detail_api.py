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
from drf_spectacular.utils import extend_schema

from domain.news.selectors import news_get
from domain.news.serializers import OutputNewsSerializer


@extend_schema(
    summary="Obtém os detalhes de uma notícia",
    tags=["Notícias"],
    responses={200: OutputNewsSerializer, 404: {"detail": "Notícia não encontrada"}},
)
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def news_detail_api(request, pk):
    if not request.user.has_perm("news.view_news"):
        raise PermissionDenied
    news = news_get(news_id=pk)

    serializer = OutputNewsSerializer(news)

    return Response(status=status.HTTP_200_OK, data=serializer.data)
