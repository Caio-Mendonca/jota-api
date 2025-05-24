from django.urls import path

from .apis.file_create_api import FileCreateApi
from .apis.file_detail_api import file_detail_api
from .apis.file_update_api import file_update_api
from .apis.file_delete_api import file_delete_api

urlpatterns = [
    path("create/", FileCreateApi.as_view(), name="create"),
    path("<int:pk>/", file_detail_api, name="detail"),
    path("<int:pk>/update/", file_update_api, name="update"),
    path("<int:pk>/delete/", file_delete_api, name="delete"),
]