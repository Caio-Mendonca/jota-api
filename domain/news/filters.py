from django_filters import rest_framework as filters
from domain.news.models import News

class NewsFilter(filters.FilterSet):
    class Meta:
        model = News
        fields = {
            'status': ['exact'],
            'access_pro': ['exact'],
            'author': ['exact'],
            'vertical': ['exact'],
            'publication_date': ['gte', 'lte'],
        }
