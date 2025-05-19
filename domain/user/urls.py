from django.urls import path

from .apis.user_delete_api import user_delete_api
from .apis.user_create_api import user_create_api
from .apis.user_detail_api import user_detail_api
from .apis.user_list_api import user_list_api
from .apis.user_update_api import user_update_api

urlpatterns = [
    path("create/", user_create_api, name="create"),
    path("<int:pk>/update/", user_update_api, name="update"),
    path("<int:pk>/delete/", user_delete_api, name="delete"),
    path("<int:pk>/", user_detail_api, name="detail"),
    path("", user_list_api, name="list"),
]
