import json
from urllib.request import urlopen
from urllib.error import URLError

class Response:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code

    def json(self):
        return json.loads(self._data)


def get(url, timeout=5):
    try:
        with urlopen(url, timeout=timeout) as resp:
            data = resp.read().decode('utf-8')
        return Response(data, 200)
    except URLError as e:
        raise ConnectionError(str(e))
