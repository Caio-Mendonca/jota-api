from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class InvalidUser(APIException, ValueError):
    status_code = 400
    default_detail = ValueError
    default_code = "invalid"


class PasswordIncorrect(APIException):
    status_code = 400
    default_detail = _(
        "Your old password was entered incorrectly. Please enter it again."
    )
    default_code = "password_incorrect"


class PasswordMismatch(APIException):
    status_code = 400
    default_detail = _("Senhas devem ser iguais.")
    default_code = "password_mismatch"


class InvalidUidUser(APIException):
    status_code = 404
    default_detail = _("O uid não representa um usuário existente.")
    default_code = "invalid_uid_user"


class InvalidToken(APIException):
    status_code = 400
    default_detail = _("Token fornecido é inválido.")
    default_code = "invalid_token"
