from django.contrib.auth.models import Group
from django_filters import rest_framework as filters


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = ["name"]
