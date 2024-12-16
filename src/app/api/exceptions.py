from fastapi import HTTPException, status


class AppException(HTTPException):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Common app exception"
    headers: dict[str, str] | None = None

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers
        )


class TokenExpiredException(AppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenNotCorrectException(AppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Not correct token format"
    headers: dict[str, str] | None = {"WWW-Authenticate": "Bearer"}
