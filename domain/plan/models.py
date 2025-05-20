
from domain.user.models import User
from support.models import BaseModel
from django.db import models


class Plan(BaseModel):
    """
    Plan model to store plan information.
    """
    class Meta:
        db_table = "plan"
        ordering = ["-created_at"]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="plans_created",
    )
    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="plans_updated",
    )


    def __str__(self):
        return self.name