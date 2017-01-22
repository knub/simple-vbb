import json
import requests

ACCESS_KEY_FILE = 'access_key.txt'


class Vbb:

    def __init__(self):
        try:
            self.access_key = self._read_access_key()
        except:
            raise Exception('Expecting access key file %s' % ACCESS_KEY_FILE)
        self.base_request = {
            'accessId': self.access_key,
            'lang': 'en',
            'format': 'json',
        }

    def _read_access_key(self):
        with open('access_key.txt', 'r') as f:
            return f.read().replace('\n', '')

    def get_station_ext_id(self, search_str):
        params = self.base_request.copy()
        params["input"] = search_str
        r = requests.get('http://demo.hafas.de/openapi/vbb-proxy/location.name', params=params)
        j = json.loads(r.text)
        station_ext_id = j["stopLocationOrCoordLocation"][0]["StopLocation"]["extId"]
        return station_ext_id

    def get_trip(self, from_ext_id, to_ext_id):
        params = self.base_request.copy()
        params["originExtId"] = from_ext_id
        params["destExtId"] = to_ext_id

        r = requests.get('http://demo.hafas.de/openapi/vbb-proxy/trip', params=params)
        with open("debug.json", "w") as f:
            json.dump(r.json(), f)
        return r.json()["Trip"]
        # return json.dumps(r.json()["Trip"], indent=4)
