from typing import Optional
from django.db import transaction
from domain.plan.models import Plan
from domain.user.models import User
from support.actions import model_update


def plan_create(
    *, name: str, description: str, created_by: Optional[User] = None
) -> Plan:
    plan = Plan(
        name=name,
        description=description,
        created_by=created_by,
        updated_by=created_by,
    )

    plan.full_clean()
    plan.save()

    return plan


@transaction.atomic
def plan_update(*, plan: Plan, data: dict, modified_by: Optional[User] = None) -> Plan:
    updatable_fields = ["name", "description"]

    plan, has_updated = model_update(
        instance=plan,
        fields=updatable_fields,
        data=data,
    )

    if has_updated:
        plan.updated_by = modified_by
        plan.full_clean()
        plan.save()

    return plan
