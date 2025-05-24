from django.db.models.query import QuerySet
from .models import Plan
from .filters import PlanFilter

def plan_list(*, filters: dict = None, request) -> QuerySet[Plan]:
    filters = filters or {}

    qs = Plan.objects.all()

    return PlanFilter(request=request, data=filters, queryset=qs).qs

def plan_get(*, plan_id: int) -> Plan:
    plan = Plan.objects.get(id=plan_id)

    return plan
