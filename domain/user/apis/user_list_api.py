from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from application.api.pagination import LimitOffsetPagination, get_paginated_response
from rest_framework_simplejwt.authentication import JWTAuthentication
from domain.user.selectors import user_list
from domain.user.serializers import FilterSerializer, UserOutputSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Lista de usuários",
    tags=["Usuários"],
    responses={200: UserOutputSerializer(many=True)},
)
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_list_api(request):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    if not request.user.has_perm("user.view_user"):
        raise PermissionDenied
    filters_serializer = FilterSerializer(data=request.query_params)
    filters_serializer.is_valid(raise_exception=True)

    users = user_list(filters=filters_serializer.validated_data, request=request)

    return get_paginated_response(
        pagination_class=Pagination,
        serializer_class=UserOutputSerializer,
        queryset=users,
        request=request,
    )
