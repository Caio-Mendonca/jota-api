from django.db.models import Q
from django_filters import rest_framework as filters

from .models import User


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")
    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("email", "email"),
            ("name", "name"),
        ),
    )

    class Meta:
        model = User
        fields = ["email", "name"]

    def search_filter(self, queryset, value):
        return queryset.filter(Q(email__contains=value) | Q(name__contains=value))
