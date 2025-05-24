from django.urls import path

from .apis.news_create_api import news_create_api
from .apis.news_update_api import news_update_api
from .apis.news_list_api import news_list_api
from .apis.news_delete_api import news_delete_api
from .apis.news_detail_api import news_detail_api
app_name = "news"

urlpatterns = [
    path("create/", news_create_api, name="create"),
    path("<int:pk>/update/", news_update_api, name="update"),
    path("<int:pk>/delete/", news_delete_api, name="delete"),
    path("<int:pk>/detail/", news_detail_api, name="detail"),
    path("", news_list_api, name="list"),
]
