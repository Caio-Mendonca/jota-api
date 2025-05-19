from django.urls import path, include

from .apis import group_list_api

urlpatterns = [
    path(
        "list/",
        include(
            (
                [
                    path("", group_list_api, name="list"),
                ],
                "groups",
            )
        ),
    ),
]
