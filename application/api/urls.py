from django.urls import path, include

urlpatterns = [
    path("user/", include(("domain.user.urls", "user"))),
    path("auth/", include(("application.authentication.urls", "authentication"))),
]
