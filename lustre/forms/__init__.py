import typing

from lustre.templating import template_render_engine

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
