import typing

from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    BaseUser,
)

from .global_state import current_request


class AuthUser(BaseUser):
    """
    An authentication object.

    Children must define:
        - (class method) create_from_token
        - to_token
        - (property) display_name

    And may define:
        - (async) full
    """

    @property
    def is_authenticated(self):
        return True

    def to_token(self) -> str:
        raise NotImplementedError(
            "to_token is not implemented for '{}'".format(self.__class__.__name__)
        )

    @classmethod
    def create_from_token(cls: type, token: str):
        raise NotImplementedError(
            "create_from_token is not implemented for '{}'".format(cls.__name__)
        )

    async def full(self):
        raise NotImplementedError(
            "full is not implemented for '{}'".format(self.__class__.__name__)
        )


class LustreAuthBackend(AuthenticationBackend):
    def __init__(self, user_type: typing.Type[AuthUser]):
        assert issubclass(
            user_type, AuthUser
        ), f"{user_type.__name__} is not an AuthUser!"
        self.user_type = user_type

    def log_in(self, user: AuthUser):
        assert isinstance(
            user, self.user_type
        ), f"The given user is not a(n) {self.user_type.__name__}"
        current_request().session["lustre_auth_token"] = user.to_token()

    def log_out(self):
        session = current_request().session
        if "lustre_auth_token" in session:
            del session["lustre_auth_token"]

    def create_user(self, token):
        return self.user_type.create_from_token(token)

    async def authenticate(self, request):
        if auth_token := request.session.get("lustre_auth_token"):
            return (
                AuthCredentials(["authenticated"]),
                self.create_user(auth_token),
            )


class AuthAppMixin:
    def setup_auth(self, user_type: typing.Type[AuthUser]):
        self.auth = LustreAuthBackend(user_type)
        self.append_middleware(AuthenticationMiddleware, backend=self.auth)
        return user_type  # Return the user type so that we can use @app.setup_auth as a decorator
