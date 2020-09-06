import os.path
import typing

from starlette.applications import Starlette, BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware

from .global_state import GlobalStateMiddleware
from .templating import set_template_global
from .config import Config
from .database import Database, DatabaseURL
from .precomputation import Precomputation
from .minification import install_html_minification_hooks


class Lustre(Starlette):
    def __init__(self, config_files=(".env", ".env.secrets")):
        super().__init__(middleware=[Middleware(GlobalStateMiddleware)])

        self.config = Config()
        for config_file in config_files:
            if os.path.isfile(config_file):
                self.config.file_values.update(self.config._read_file(config_file))

    def setup_database(self, database_url: typing.Union[str, DatabaseURL]):
        self.db = Database(database_url)

    def setup_precomputation(self, precomp_package: str):
        self.precomputation = Precomputation(precomp_package)
        set_template_global("precomp", self.precomputation)

    def setup_html_minification(self, **config):
        install_html_minification_hooks(**config)

    def add_static_folder(
        self, directory: str, path: str = None, name: str = None, **kwargs
    ):
        if path is None:
            path = "/" + directory

        self.mount(path, StaticFiles(directory=directory, **kwargs), name)
