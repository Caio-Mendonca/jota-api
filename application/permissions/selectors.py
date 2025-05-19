from django.db.models.query import QuerySet
from django.conf import settings

from django.contrib.auth.models import Group
from .filters import GroupFilter


def group_list(*, filters: dict = None) -> QuerySet[Group]:
    filters = filters or {}

    qs = Group.objects.all().order_by("id")

    return GroupFilter(filters, qs).qs


def group_get(group_id: int):
    group = Group.objects.get(pk=group_id)

    return group
