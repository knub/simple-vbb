import json
import requests


def read_access_key():
    with open('access_key.txt', 'r') as f:
        return f.read().replace('\n', '')

params = {
    'accessId': read_access_key(),
    'lang': 'en',
    'format': 'json',

    'input': 'S Wannsee'
}
r = requests.get('http://demo.hafas.de/openapi/vbb-proxy/location.name', params=params)
j = json.loads(r.text)
print(json.dumps(j, indent=4, sort_keys=True))
