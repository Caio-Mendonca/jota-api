from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from domain.vertical.actions import vertical_create
from domain.vertical.serializers import  CreateVerticalSerializer, VerticalOutputSerializer
from django.core.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Cria uma nova vertical",
    tags=["Verticais"],
    request=CreateVerticalSerializer,
    responses={201: None},
)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def vertical_create_api(request):
    if not request.user.has_perm("vertical.add_vertical"):
        raise PermissionDenied
    serializer = CreateVerticalSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    vertical = vertical_create(**serializer.validated_data, user=request.user)
    serializer = VerticalOutputSerializer(vertical) 

    return Response(serializer.data, status=status.HTTP_201_CREATED)


