from starlette.config import Config as StarletteConfig
from .templating import register_template_global

from starlette.datastructures import Secret, CommaSeparatedStrings


class Config(StarletteConfig):
    def get(self, key: str, *args, **kwargs):
        result = super().get(key, *args, **kwargs)
        register_template_global(key, result)
        return result
