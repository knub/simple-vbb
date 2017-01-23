from flask import Flask, render_template
import re

from simple_vbb.vbb import Vbb, DummyVbb

app = Flask(__name__)
# vbb = Vbb()
vbb = DummyVbb()

FROM = "S Nikolassee"
FROM = "Pfaueninselchausee"
FROM = "S Wannsee"
TO = "Ahrensfelde"
TO = "U Stadtmitte"
FROM_ID = vbb.get_station_ext_id(FROM)
TO_ID = vbb.get_station_ext_id(TO)


class TripsViewModel:

    def __init__(self, trips):
        self.trips = trips

        # removes underground suffix from station names, e.g. "U Stadtmitte U2" --> "U Stadtmitte"
        self.remove_u_regex = re.compile(" U\\d")
        self.augment_trips()

    def clean_station_name(self, s):
        s = s \
            .replace(" (Bln)", "") \
            .replace(" (Berlin)", "") \
            .replace(" Bhf", "") \
            .replace("[", "") \
            .replace("]", "") \

        s = self.remove_u_regex.sub("", s)
        return s.strip()

    def augment_trips(self):
        for trip in self.trips:
            trip["duration"] = trip["duration"].replace("PT", "").replace("M", "")
            for leg in trip["LegList"]["Leg"]:
                # Fix
                leg["Origin"]["name"] = self.clean_station_name(leg["Origin"]["name"])
                leg["Destination"]["name"] = self.clean_station_name(leg["Destination"]["name"])
                # Fix time
                leg["Origin"]["time"] = leg["Origin"]["time"][:-3]
                leg["Destination"]["time"] = leg["Destination"]["time"][:-3]
                leg["name"] = leg["name"].replace("Bus ", "B").strip()

    def __iter__(self):
        return iter(self.trips)


@app.route("/")
def root():
    text = vbb.get_trip(FROM_ID, TO_ID)
    return render_template("main.html", text=text)


@app.route("/trips")
def trips():
    trips = TripsViewModel(vbb.get_trip(FROM_ID, TO_ID))
    return render_template("trips.html", trips=trips, from_station=FROM, to_station=TO)

if __name__ == "__main__":
    app.run()
