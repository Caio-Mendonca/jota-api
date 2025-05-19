from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
    TokenObtainPairView,
)

from application.authentication.apis import user_me_api

urlpatterns = [
    path(
        "jwt/",
        include(
            (
                [
                    path("login/", TokenObtainPairView.as_view(), name="login"),
                    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
                    path("logout/", TokenBlacklistView.as_view(), name="logout"),
                ],
                "jwt",
            )
        ),
    ),
    path("me/", user_me_api, name="me"),
]
