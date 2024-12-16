from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

from app.api.admin.exceptions import NotCorrectSuperadminToken
from app.api.exceptions import TokenExpiredException, TokenNotCorrectException
from config import Config, get_config


def verify_superadmin(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    config: Config = Depends(get_config),
) -> dict:
    try:
        payload = jwt.decode(credentials.credentials, config.auth.PUBLIC_KEY, config.auth.ALGORITHM)
        if payload.get("sub") != "0" or payload.get("name") != "superadmin":
            raise NotCorrectSuperadminToken
        return payload
    except (ExpiredSignatureError, JWTError) as e:
        if isinstance(e, ExpiredSignatureError):
            raise TokenExpiredException
        else:
            raise TokenNotCorrectException
