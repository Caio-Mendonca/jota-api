import re
from typing import Optional
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
    Group,
)
from django.core.exceptions import ValidationError
from support.models import BaseModel


def check_string_is_number(value: str):
    reg = re.compile(r"^-?\d+\Z")
    if not reg.match(value):
        raise ValidationError("Valor precisa ser um número válido.")


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        name: str,
        group: Group,
        is_active: bool = False,
        password: Optional[str] = None,
        is_admin: bool = False,
    ):
        user = self.model(
            email=self.normalize_email(email.lower()),
            name=name,
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        user.groups.add(group)
        return user

    def create_superuser(
        self,
        email: str,
        name: str,
        password: str = None,
    ):
        default_group = Group.objects.get(name=settings.GROUP_ADM)
        user = self.create_user(
            email=email,
            name=name,
            is_active=True,
            password=password,
            is_admin=True,
            group=default_group,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "user"
        ordering = ["-created_at"]
        permissions = [
            ("can_add_group_to_user", "Can add groups to a user"),
        ]

    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"

    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f"{self.name} - {self.email}"
