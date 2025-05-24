from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from application.authentication.apis import user_me_api


@extend_schema_view(post=extend_schema(summary="Login com JWT", tags=["Autenticação"]))
class LoginView(TokenObtainPairView):
    pass


@extend_schema_view(
    post=extend_schema(summary="Atualiza o token JWT", tags=["Autenticação"])
)
class RefreshTokenView(TokenRefreshView):
    pass


@extend_schema_view(
    post=extend_schema(summary="Faz logout (blacklist no token)", tags=["Autenticação"])
)
class LogoutView(TokenBlacklistView):
    pass


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "me/",
        extend_schema(
            summary="Retorna os dados do usuário autenticado",
            tags=["Autenticação"],
        )(user_me_api),
        name="me",
    ),
]
