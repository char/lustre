from starlette.middleware.sessions import SessionMiddleware

class SessionAppMixin:
    def __init__(self):
        pass

    def setup_sessions(self, secret_key: str, **kwargs):
        self.append_middleware(SessionMiddleware, secret_key=secret_key, **kwargs)

