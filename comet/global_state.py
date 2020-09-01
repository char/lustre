current_request = None


class GlobalStateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, next):
        global current_request
        current_request = request

        return await next(request)
