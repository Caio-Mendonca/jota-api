from rest_framework_simplejwt.tokens import RefreshToken
from domain.user.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class TokenGenerator(PasswordResetTokenGenerator):
    pass


generate_token = TokenGenerator()
