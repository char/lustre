from starlette.config import Config as StarletteConfig
from .templating import set_template_global

from starlette.datastructures import Secret, CommaSeparatedStrings


class Config(StarletteConfig):
    def get(self, key: str, *args, **kwargs):
        result = super().get(key, *args, **kwargs)
        set_template_global(key, result)
        return result
