from django.db import models
from domain.plan.models import Plan
from domain.user.models import User
from support.models import BaseModel

class Vertical(BaseModel):
    class Meta:
        db_table = "vertical"
        ordering = ["-created_at"]

    name = models.CharField(max_length=255, unique=True)

    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verticals_created"
    )

    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verticals_updated"
    )

    def __str__(self):
        return self.name

class PlanVertical(BaseModel):
    class Meta:
        db_table = "plan_vertical"
        ordering = ["-created_at"]

    plan = models.ForeignKey(
        to=Plan,
        on_delete=models.CASCADE,
        related_name="plan_verticals"
    )

    vertical = models.ForeignKey(
        to=Vertical,
        on_delete=models.CASCADE,
        related_name="plan_verticals"
    )

    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plan_verticals_created"
    )

    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plan_verticals_updated"
    )

    def __str__(self):
        return f"{self.plan.name} - {self.vertical.name}"