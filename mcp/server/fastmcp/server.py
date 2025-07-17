from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from starlette.requests import Request

ServerSessionT = TypeVar("ServerSessionT")
LifespanContextT = TypeVar("LifespanContextT")
RequestT = TypeVar("RequestT", bound=Request)

class Context(BaseModel, Generic[ServerSessionT, LifespanContextT, RequestT]):
    request: Optional[RequestT] = None
    session: Optional[ServerSessionT] = None
    lifespan: Optional[LifespanContextT] = None

    class Config:
        arbitrary_types_allowed = True

    def get_user(self):
        if hasattr(self.request, "user"):
            return self.request.user
        return None

    def is_authenticated(self):
        user = self.get_user()
        return user is not None and getattr(user, "is_authenticated", False)

class FastMCP:
    def __init__(self, app_name: str, lifespan=None):
        self.app_name = app_name
        self.lifespan = lifespan

    def tool(self):
        def decorator(func):
            return func
        return decorator

    def prompt(self):
        def decorator(func):
            return func
        return decorator

