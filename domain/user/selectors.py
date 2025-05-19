from django.db.models.query import QuerySet

from .models import User
from .filters import UserFilter


def user_list(*, filters: dict = None, request) -> QuerySet[User]:
    filters = filters or {}

    qs = User.objects.all()

    return UserFilter(request=request, data=filters, queryset=qs).qs


def user_get(*, user_id: int) -> User:
    user = User.objects.get(id=user_id)

    return user


def user_get_email(*, user_email: str) -> User:
    user = User.objects.get(email=user_email)

    return user
