from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app.api.exceptions import TokenExpiredException, TokenNotCorrectException
from app.api.schemas import UserSchema
from config import Config, get_config


class AuthCredentials:
    """
    Зависимость, подтверждающая аутентификацию юзера через JWT.
    Возвращает даные о юзере, полученные в payload токена
    """

    def __init__(self, config: Config) -> None:
        self.config = config

    def __call__(
        self,
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    ) -> UserSchema:
        """
        :param credentials: Зависимость из FastAPI security. Проверяет наличие заголовка "Authorization" и схемы Bearer.
        Возвращает схему и сам токен
        :return: Данные о пользователе, полученные из payload токена
        """
        try:
            payload = jwt.decode(
                credentials.credentials,
                self.config.auth.PUBLIC_KEY,
                self.config.auth.ALGORITHM
            )
            user_data = UserSchema(**payload)
            if not user_data:
                raise TokenNotCorrectException(status_code=401, detail="Token is not correct")

            return user_data

        except (ExpiredSignatureError, JWTError) as e:
            if isinstance(e, ExpiredSignatureError):
                raise TokenExpiredException(status_code=401, detail="Token is expired")
            else:
                raise TokenNotCorrectException(status_code=401, detail="Token is not correct")


def get_user() -> AuthCredentials:
    return AuthCredentials(config=get_config())
