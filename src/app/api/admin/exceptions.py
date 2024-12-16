from fastapi import status

from app.api.exceptions import AppException


class NotCorrectSuperadminToken(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token not belong to superadmin"
