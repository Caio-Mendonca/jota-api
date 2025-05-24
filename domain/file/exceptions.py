from rest_framework.exceptions import APIException


class InvalidImageFormat(APIException):
    status_code = 400
    default_detail = "O formato de imagem é inválido."
    default_code = "invalid_image"


class InvalidAttachmentFormat(APIException):
    status_code = 400
    default_detail = "O formato do arquivo é inválido."
    default_code = "invalid_image"