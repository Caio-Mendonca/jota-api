from django.db.models.query import QuerySet
from domain.news.models import News
from domain.news.filters import NewsFilter
from domain.user.models import User
from domain.vertical.models import Vertical

def news_list(*, filters: dict = None, request) -> QuerySet[News]:
    filters = filters or {}

    qs = News.objects.all()

    return NewsFilter(request=request, data=filters, queryset=qs).qs


def news_get(*, news_id: int) -> News:
    return News.objects.get(id=news_id)


def news_get_by_title(*, title: str) -> News:
    return News.objects.get(title=title)
