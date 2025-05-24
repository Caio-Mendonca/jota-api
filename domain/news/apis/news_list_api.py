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
from application.api.pagination import LimitOffsetPagination, get_paginated_response
from domain.news.selectors import news_list
from domain.news.serializers import  OutputNewsSerializer
from domain.user.serializers import FilterSerializer


@extend_schema(
    summary="Lista as notícias",
    tags=["Notícias"],
    responses={200: OutputNewsSerializer, 403:PermissionDenied},
)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def news_list_api(request):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    if not request.user.has_perm("news.view_news"):
        raise PermissionDenied
    filters_serializer = FilterSerializer(data=request.query_params)
    filters_serializer.is_valid(raise_exception=True)
    news = news_list(filters=filters_serializer.validated_data, request=request)
    return get_paginated_response(
        pagination_class=Pagination,
        serializer_class=OutputNewsSerializer,
        queryset=news,
        request=request,
    )

