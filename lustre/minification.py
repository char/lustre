import typing

from starlette.responses import Response, HTMLResponse
from starlette.templating import _TemplateResponse

try:
    import htmlmin
except ImportError:
    htmlmin = None


def install_html_minification_hooks(
    response_classes=[HTMLResponse, _TemplateResponse], **minification_config
):
    assert htmlmin is not None, "htmlmin must be installed to use HTML minification"

    original_render = Response.render

    def minify_and_render(self, content: typing.Any) -> bytes:
        if isinstance(content, str):
            minified_content = htmlmin.minify(content, **minification_config)
            return original_render(self, minified_content)

        return original_render(self, content)

    for response_class in response_classes:
        response_class.render = minify_and_render
