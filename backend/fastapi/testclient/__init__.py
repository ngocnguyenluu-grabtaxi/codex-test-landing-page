from types import SimpleNamespace

class Response:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data
    def json(self):
        return self._data

class TestClient:
    def __init__(self, app):
        self.app = app

    def _call(self, method, path, params=None):
        # Try direct match
        func = self.app._routes.get((method, path))
        kwargs = params or {}
        if not func:
            # attempt path parameter substitution
            for (m, p), f in self.app._routes.items():
                if m != method:
                    continue
                if '{' in p and path.startswith(p.split('{')[0]):
                    param_name = p[p.find('{')+1:p.find('}')]
                    param_value = path[len(p.split('{')[0]):]
                    kwargs[param_name] = param_value
                    func = f
                    break
        if not func:
            return Response(404, {'detail': 'Not Found'})
        try:
            result = func(**kwargs)
            status_code = 200
        except Exception as e:
            if hasattr(e, 'status_code'):
                status_code = e.status_code
                result = {'detail': e.detail}
            else:
                status_code = 500
                result = {'detail': str(e)}
        return Response(status_code, result)

    def get(self, path, params=None):
        return self._call('GET', path, params)

    def post(self, path, params=None):
        return self._call('POST', path, params)

    def delete(self, path, params=None):
        return self._call('DELETE', path, params)
