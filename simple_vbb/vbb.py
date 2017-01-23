from datetime import datetime
import json
import requests

ACCESS_KEY_FILE = 'access_key.txt'


class AccessKeyMissingException(Exception):
    pass


class Vbb:

    def __init__(self):
        try:
            self.access_key = self._read_access_key()
        except:
            raise AccessKeyMissingException('Expecting access key file %s' % ACCESS_KEY_FILE)

    def build_base_request(self):
        now = datetime.now()
        return {
            'accessId': self.access_key,
            'lang': 'en',
            'format': 'json',
            'date': now.strftime("%Y-%m-%d"),
            'time': now.strftime("%H:%M"),
        }

    def _read_access_key(self):
        with open('access_key.txt', 'r') as f:
            return f.read().replace('\n', '')

    def get_station_ext_id(self, search_str):
        params = self.build_base_request()
        params.update({
            'input': search_str,
        })
        r = requests.get('http://demo.hafas.de/openapi/vbb-proxy/location.name', params=params)
        station_ext_id = r.json()["stopLocationOrCoordLocation"][0]["StopLocation"]["extId"]
        return station_ext_id

    def get_trip(self, from_ext_id, to_ext_id):
        params = self.build_base_request()
        params.update({
            'originExtId': from_ext_id,
            'destExtId': to_ext_id,
        })

        r = requests.get('http://demo.hafas.de/openapi/vbb-proxy/trip', params=params)
        with open("debug.json", "w") as f:
            json.dump(r.json(), f)

        trips = r.json()["Trip"]
        return trips


class DummyVbb:
    """
    Dummy version of the VBB api, which returns fixed response from disk instead of calling the API.
    Useful for debugging or styling the CSS without bothering the server.
    """

    def get_trip(self, from_ext_id, to_ext_id):
        with open("sample_responses/delay.json") as f:
            return json.load(f)["Trip"]

    def get_station_ext_id(self, search_str):
        return ""
