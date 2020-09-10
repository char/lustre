import typing
import asyncio
import functools

from ..templating import template_render_engine
from ..responses import redirect

from typesystem import Jinja2Forms as TypeSystemForms, Schema, ValidationError
from typesystem import (
    Any,
    Array,
    Boolean,
    Choice,
    Date,
    DateTime,
    Decimal,
    Field,
    Float,
    Integer,
    Number,
    Object,
    String,
    Text,
    Time,
    Union,
)

form_render_engine = TypeSystemForms(package="lustre.forms")
form_render_engine.env = template_render_engine.env


def render_form(
    schema: typing.Type[Schema], values: dict = None, errors: ValidationError = None
):
    return form_render_engine.Form(schema, values=values, errors=errors)


class FormsAppMixin:
    def __init__(self):
        self.form_renderer_cache = {}

    def form_renderer(self, form_type: typing.Type[Schema], path: str, *args, **kwargs):
        def _render_form(request):
            last_form_type = request.session.pop("last_form_type", None)
            if last_form_type == form_type.__qualname__:
                form_values = request.session.pop("last_form_values", None)
                form_errors = request.session.pop("last_form_errors", None)
            else:
                form_values = None
                form_errors = None

            return render_form(form_type, values=form_values, errors=form_errors)

        def decorator(func):
            self.form_renderer_cache[form_type] = path

            if asyncio.iscoroutinefunction(func):

                @functools.wraps(func)
                async def wrapper(request, *args, **kwargs):
                    form = _render_form(request)
                    return await func(request, form, *args, **kwargs)

            else:

                @functools.wraps(func)
                def wrapper(request, *args, **kwargs):
                    form = _render_form(request)
                    return func(request, form, *args, **kwargs)

            return self.route(path, *args, **kwargs)(wrapper)

        return decorator

    def form_handler(self, form_type: typing.Type[Schema], path: str, *args, **kwargs):
        def decorator(func):
            assert asyncio.iscoroutinefunction(
                func
            ), "Form handlers must be asynchronous!"

            @functools.wraps(func)
            async def wrapper(request, *args, **kwargs):
                request.session.pop("last_form_values", None)
                request.session.pop("last_form_errors", None)

                request.session["last_form_type"] = form_type.__qualname__

                try:
                    parsed_form = form_type.validate(await request.form())
                    response = await func(request, parsed_form, *args, **kwargs)
                    if response is not None:
                        return response
                except ValidationError as errors:
                    request.session["last_form_errors"] = dict(errors)
                    request.session["last_form_values"] = dict(await request.form())

                assert (
                    form_type in self.form_renderer_cache
                ), f"No renderer for '{form_type.__name__}'"
                return redirect(self.form_renderer_cache[form_type])

            return self.route(path, *args, **kwargs)(wrapper)

        return decorator
