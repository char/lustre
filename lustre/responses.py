from starlette.responses import (
    PlainTextResponse,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
)


plain = PlainTextResponse
html = HTMLResponse
json = JSONResponse


def redirect(location, status_code=303, **kwargs):
    return RedirectResponse(location, status_code=status_code, **kwargs)
