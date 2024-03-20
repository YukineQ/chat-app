from abc import ABC, abstractmethod
from typing import Any, Type

from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi import Request
from fastapi.security.base import SecurityBase
from starlette import status

from app.container import Container
from app.user.domain.usecase.user import UserUseCase
from core.exceptions import ExceptionBase


class UnauthorizedException(ExceptionBase):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = "UNAUTHORIZED"
    message = ""


class BasePermission(ABC):
    exception = ExceptionBase

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        """has permission"""


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    @inject
    async def has_permission(
        self,
        request: Request,
        usecase: UserUseCase = Depends(Provide[Container.user_service])
    ) -> bool:
        user_id = request.user.id
        if not user_id:
            return False

        return await usecase.is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permission: list[Type[BasePermission]]):
        self.permission = permission
        self.model: APIKey = APIKey(
            **{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permission:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception
