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

from domain.news.serializers import CreateNewsSerializer, OutputNewsSerializer
from domain.news.actions import news_create
from django.core.exceptions import PermissionDenied


@extend_schema(
    summary="Cria uma nova notícia",
    tags=["Notícias"],
    request=CreateNewsSerializer,
    responses={201: OutputNewsSerializer},
)

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def news_create_api(request):
    if not request.user.has_perm("plan.add_news"):
        raise PermissionDenied

    serializer = CreateNewsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    new = news_create(**serializer.validated_data, created_by=request.user)

    serializer = OutputNewsSerializer(new)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
