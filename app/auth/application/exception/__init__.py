from core.exceptions import ExceptionBase


class DecodeTokenException(ExceptionBase):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(ExceptionBase):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"
