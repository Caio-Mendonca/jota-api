from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Plan


class PlanFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")
    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("created_by", "created_by"),
            ("name", "name"),
        ),
    )

    class Meta:
        model = Plan
        fields = [ "name"]

    def search_filter(self, queryset, value):
        return queryset.filter(Q(name__contains=value))
