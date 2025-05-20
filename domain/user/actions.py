from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from typing import Optional
from django.contrib.auth.models import Group
from django.db import transaction
from domain.user.exceptions import InvalidUser
from .models import User
from support.actions import model_update


def user_create(
    *,
    email: str,
    name: str,
    group: Group,
    password: Optional[str] = None,
    is_active: bool = True,
) -> User:
    user = User.objects.create_user(
        email=email,
        name=name,
        password=password,
        group=group,
        is_active=is_active,
    )

    user.save()

    return user


@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = [
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
        user.save()
        user.groups.add(data["group"])

    return user
