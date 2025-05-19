from rest_framework import serializers, status
from rest_framework.decorators import (
    api_view,
)
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from domain.user.actions import user_activate_and_create_password


class InputSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        label=_("New password"),
        write_only=True,
        style={"input_type": "password"},
    )
    confirm_password = serializers.CharField(
        required=True,
        label=_("New password confirmation"),
        help_text=_("Enter the same password as before, for verification."),
        write_only=True,
        style={"input_type": "password"},
    )


@api_view(["POST"])
def user_activate_and_create_password_api(request, uid):
    serializer = InputSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_activate_and_create_password(
        uid=uid, token=request.data["token"], data=serializer.validated_data
    )

    return Response(status=status.HTTP_200_OK)
