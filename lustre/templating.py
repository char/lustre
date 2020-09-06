import typing

from starlette.templating import Jinja2Templates as StarletteTemplates
from starlette.responses import Response

from jinja2 import ChoiceLoader, FileSystemLoader, PackageLoader

from lustre.global_state import current_request

template_render_engine = StarletteTemplates("templates")
template_render_engine.env.loader = ChoiceLoader(
    [
        FileSystemLoader("templates"),
        PackageLoader("lustre.forms", "templates"),
    ]
)


def template_filter(name: str):
    """
    Register a template filter. Used as a decorator:

    .. codeblock:: python
        @template_filter("markdown")
        def markdown(text):
            from XYZ import commonmark
            return commonmark(text)
    """

    def decorator(func):
        template_render_engine.env.filters[name] = func
        return func

    return decorator


def set_template_global(name: str, value: typing.Any):
    template_render_engine.env.globals[name] = value


def render_template(
    template_name: str, context: dict = None, status_code: int = 200, **kwargs
) -> Response:
    """
    Render a template from the 'templates' directory.

    The current request is automatically added to the context.
    """

    if context is None:
        context = {}
    context.update({"request": current_request()})

    return templating_engine.TemplateResponse(
        template_name, context, status_code=status_code, **kwargs
    )
