from django.urls import path
from .apis import group_list_api

app_name = "groups"

urlpatterns = [
    path("list/", group_list_api, name="list"),
]
