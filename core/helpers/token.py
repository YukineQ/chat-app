from datetime import datetime, timedelta

import jwt

from core.config import config
from core.exceptions import ExceptionBase

class DecodeTokenException(ExceptionBase):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(ExceptionBase):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"


class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 3600) -> str:
        token = jwt.encode(
            payload={
                **payload,
                "exp": datetime.now() + timedelta(seconds=expire_period),
            },
            key=config.JWT_SECRET,
            algorithm=config.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET,
                config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpireSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
