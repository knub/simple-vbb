import json
import requests


class Vbb:

    def __init__(self):
        pass

    def foo(self):
        return "Hallo Welt"

    def read_access_key(self):
        with open('access_key.txt', 'r') as f:
            return f.read().replace('\n', '')

    def demo(self):
        params = {
            'accessId': self.read_access_key(),
            'lang': 'en',
            'format': 'json',

            'input': 'S Wannsee'
        }
        r = requests.get('http://demo.hafas.de/openapi/vbb-proxy/location.name', params=params)
        j = json.loads(r.text)
        print(json.dumps(j, indent=4, sort_keys=True))
