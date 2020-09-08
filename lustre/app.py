import os.path
import typing

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware

from .global_state import GlobalStateMiddleware
from .config import ConfigAppMixin
from .database import DatabaseAppMixin
from .precomputation import PrecomputationAppMixin
from .sessions import SessionAppMixin
from .auth import AuthAppMixin
from .forms import FormsAppMixin


class Lustre(
    Starlette,
    ConfigAppMixin,
    DatabaseAppMixin,
    PrecomputationAppMixin,
    SessionAppMixin,
    AuthAppMixin,
    FormsAppMixin,
):
    def __init__(self, config_files=(".env", ".env.secrets")):
        Starlette.__init__(self, middleware=[Middleware(GlobalStateMiddleware)])
        ConfigAppMixin.__init__(self, config_files)
        DatabaseAppMixin.__init__(self)
        PrecomputationAppMixin.__init__(self)
        SessionAppMixin.__init__(self)
        AuthAppMixin.__init__(self)
        FormsAppMixin.__init__(self)

    def append_middleware(self, middleware_class: type, **options: typing.Any) -> None:
        self.user_middleware.append(Middleware(middleware_class, **options))
        self.middleware_stack = self.build_middleware_stack()

    def add_static_folder(
        self, directory: str, path: str = None, name: str = None, **kwargs
    ):
        if path is None:
            path = "/" + directory

        self.mount(path, StaticFiles(directory=directory, **kwargs), name)
