from django.urls import path, include

app_name = "api"

urlpatterns = [
    path("files/", include(("domain.file.urls", "files"))),
    path("vertical/", include(("domain.vertical.urls", "vertical"))),
    path("news/", include(("domain.news.urls", "news"))),
    path("user/", include(("domain.user.urls", "user"))),
    path("plan/", include(("domain.plan.urls", "plan"))),
    path("auth/", include(("application.authentication.urls", "auth"))),
    path("groups/", include(("application.permissions.urls", "groups"))),
]
