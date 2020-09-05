from starlette.middleware.base import BaseHTTPMiddleware

_current_request = None


def current_request():
    return _current_request


class GlobalStateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, next):
        global _current_request
        _current_request = request
        return await next(request)
