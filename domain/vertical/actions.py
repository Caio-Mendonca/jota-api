from domain.plan.models import Plan
from domain.vertical.models import PlanVertical, Vertical
from domain.user.models import User

def vertical_create(
    *,
    name: str,
    user: User
) -> Vertical:
    vertical = Vertical.objects.create(
        name=name,
        created_by=user,
    )
    return vertical

def plan_vertical_create(
    *,
    plan: Plan,
    vertical: Vertical,
    user: User = None
) -> PlanVertical:
    plan_vertical = PlanVertical.objects.create(
        plan=plan,
        vertical=vertical,
        created_by=user,
    )
    return plan_vertical