from django.db import models
from domain.user.models import User
from support.models import BaseModel
from domain.file.models import File  
from domain.vertical.models import Vertical 

class NewsStatus(models.TextChoices):
    DRAFT = 'draft', 'draft'
    PUBLISHED = 'published', 'published'
    ARCHIVED = 'archived', 'archived'

class News(BaseModel):

    class Meta:
        db_table = "news"
        ordering = ["-created_at"]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    
    image = models.ForeignKey(
        to=File,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="news_images",
    )
    
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="news_authored",
    )
    
    publication_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Permite agendamento de publicação",
    )
    
    status = models.CharField(
        max_length=20,
        choices=NewsStatus.choices,
        default=NewsStatus.DRAFT,
    )
    
    access_pro = models.BooleanField(default=False)
    
    vertical = models.ForeignKey(
        to=Vertical,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="news_verticals",
    )
    
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="news_created",
    )
    
    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name="news_updated",
    )

    def __str__(self):
        return self.title
