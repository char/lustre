import typing
import os

from starlette.config import Config as StarletteConfig
from .templating import set_template_global

from starlette.datastructures import Secret, CommaSeparatedStrings


class Config(StarletteConfig):
    def get(self, key: str, *args, **kwargs):
        result = super().get(key, *args, **kwargs)
        set_template_global(key, result)
        return result


class ConfigAppMixin:
    def __init__(self, config_files: typing.Sequence[str]):
        self.config = Config()
        for config_file in config_files:
            if os.path.isfile(config_file):
                self.config.file_values.update(self.config._read_file(config_file))
