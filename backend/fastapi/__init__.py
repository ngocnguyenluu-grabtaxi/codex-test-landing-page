class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class Query:
    def __init__(self, default=None, alias: str | None = None):
        self.default = default
        self.alias = alias

def _register_route(app, method, path):
    def decorator(func):
        app._routes[(method, path)] = func
        return func
    return decorator

class FastAPI:
    def __init__(self):
        self._routes = {}
    def post(self, path):
        return _register_route(self, 'POST', path)
    def get(self, path):
        return _register_route(self, 'GET', path)
    def delete(self, path):
        return _register_route(self, 'DELETE', path)
    def mount(self, path, app, name=None):
        pass

from .staticfiles import StaticFiles
