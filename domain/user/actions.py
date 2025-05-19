from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from typing import Optional
from django.contrib.auth.models import Group
from django.db import transaction
from jwt import InvalidTokenError

# from application.emails.actions import (
#     send_reset_password,
#     send_welcome_new_user_create_password,
# )
from django.utils.encoding import force_bytes
from domain.user.exceptions import InvalidUser
from .models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from support.actions import model_update
from support.utils import generate_token
from .exceptions import (
    PasswordIncorrect,
    PasswordMismatch,
    InvalidUidUser,
    InvalidToken,
)


def user_create(
    *,
    email: str,
    name: str,
    group: Group,
    password: Optional[str] = None,
    # avatar: Optional[File] = None,
    is_active: bool = False,
) -> User:
    user = User.objects.create_user(
        email=email,
        name=name,
        password=password,
        group=group,
        # avatar=avatar,
        is_active=is_active,
    )

    user.save()

    # send_welcome_new_user_create_password(
    #     {
    #         "user": {"email": user.email, "name": user.name},
    #         "token": generate_token.make_token(user),
    #         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    #     }
    # )
    return user


@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = [
        "avatar",
        "name",
        "email",
        "is_active",
    ]

    user, has_updated = model_update(
        instance=user, fields=non_side_effect_fields, data=data
    )

    if "group" in data:
        if user.groups.filter(id=data["group"].id).exists():
            return user

        group = user.groups.get()
        user.groups.remove(group)
        if data["group"].name != "Administrador":
            user.is_admin = False
        else:
            user.is_admin = True
        user.save()
        user.groups.add(data["group"])

    return user


@transaction.atomic
def user_altered_password(*, user: User, data):
    if not user.check_password(data["old_password"]):
        raise InvalidUser(ValueError("Senha antiga incorreta"))
    user.set_password(data["new_password"])
    user.save()
    return user


# @transaction.atomic
# def user_send_email_reset_password(*, user: User):
#     send_reset_password(
#         {
#             "user": {"email": user.email, "name": user.name},
#             "token": generate_token.make_token(user),
#             "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#         }
#     )
#     return user


@transaction.atomic
def user_reset_password(*, uid, token, data) -> None:
    try:
        id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        raise InvalidUidUser()

    if not generate_token.check_token(user, token):
        raise InvalidToken()

    if data.get("password") != data.get("confirm_password"):
        raise PasswordMismatch()

    user.set_password(data.get("password"))
    user.save()
    return


@transaction.atomic
def user_activate_and_create_password(*, uid, token, data) -> None:
    try:
        id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        raise InvalidUidUser()
    if not generate_token.check_token(user, token):
        raise InvalidToken()

    if data.get("password") != data.get("confirm_password"):
        raise PasswordMismatch()
    user.is_active = True
    user.set_password(data.get("password"))
    user.save()
    return
