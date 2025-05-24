from typing import Optional
from django.db import transaction
from domain.news.models import News, NewsStatus
from domain.user.models import User
from domain.file.models import File
from domain.vertical.models import Vertical
from support.actions import model_update


def news_create(
    *,
    title: str,
    content: str,
    author: User,
    vertical: Vertical,
    created_by: Optional[User] = None,
    subtitle: Optional[str] = None,
    image: Optional[File] = None,
    publication_date: Optional[str] = None,
    status: str = NewsStatus.DRAFT,
    access_pro: bool = False,
) -> News:
    news = News.objects.create(
        title=title,
        subtitle=subtitle,
        content=content,
        image=image,
        author=author,
        vertical=vertical,
        publication_date=publication_date,
        status=status,
        access_pro=access_pro,
        created_by=created_by,
    )
    return news


@transaction.atomic
def news_update(*, news: News, data) -> News:
    updatable_fields = [
        "title",
        "subtitle",
        "content",
        "image",
        "publication_date",
        "status",
        "access_pro",
        "vertical",
        "updated_by",
    ]

    news, has_updated = model_update(
        instance=news, fields=updatable_fields, data=data
    )

    return news
