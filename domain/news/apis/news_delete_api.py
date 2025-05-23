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
from domain.news.selectors import news_get
from domain.news.serializers import CreateNewsSerializer, NewsUpdateSerializer, OutputNewsSerializer
from domain.news.actions import news_create, news_update


@extend_schema(
    summary="Deletar uma notícia",
    tags=["Notícias"],
    responses={204:None},
)

@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def news_delete_api(request, pk):
    if not request.user.has_perm("news.delete_news"):
        raise PermissionDenied
    new = news_get(news_id=pk)
    new.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)