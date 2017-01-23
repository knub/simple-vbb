from datetime import datetime
from flask import Flask, render_template
import re

from simple_vbb.vbb import Vbb, DummyVbb

app = Flask(__name__)
# vbb = Vbb()
vbb = DummyVbb()

FROM = "S Nikolassee"
FROM = "Pfaueninselchausee"
FROM = "Teltow, Bahnhof"
FROM = "S Wannsee"
TO = "Ahrensfelde"
TO = "Jüterbog, Bahnhof"
TO = "U Stadtmitte"
FROM_ID = vbb.get_station_ext_id(FROM)
TO_ID = vbb.get_station_ext_id(TO)


class TripsViewModel:

    def __init__(self, trips):
        self.trips = trips

        # removes underground suffix from station names, e.g. "U Stadtmitte U2" --> "U Stadtmitte"
        self.remove_u_regex = re.compile(" U\\d")
        self.augment_trips()

    def prepare_station_names(self, leg):
        def clean_station_name(s):
            s = s \
                .replace(" (Bln)", "") \
                .replace(" (Berlin)", "") \
                .replace(" Bhf", "") \
                .replace("[", "") \
                .replace("]", "") \

            s = self.remove_u_regex.sub("", s)
            return s.strip()
        leg["Origin"]["name"] = clean_station_name(leg["Origin"]["name"])
        leg["Destination"]["name"] = clean_station_name(leg["Destination"]["name"])

    def prepare_times(self, leg):
        leg["Origin"]["time"] = leg["Origin"]["time"][:-3]
        leg["Destination"]["time"] = leg["Destination"]["time"][:-3]

    def prepare_delay_info(self, leg):
        def calculate_delay(station):
            if "rtTime" in leg[station]:
                start_planned = datetime.strptime("%s %s" % (leg[station]["date"], leg[station]["time"]), "%Y-%m-%d %H:%M:%S")
                start_actual = datetime.strptime("%s %s" % (leg[station]["rtDate"], leg[station]["rtTime"]), "%Y-%m-%d %H:%M:%S")
                return (start_actual - start_planned).total_seconds() / 60
            else:
                return None

        orig_delay = calculate_delay("Origin")
        leg["Origin"]["delay"] = orig_delay
        dest_delay = calculate_delay("Destination")
        leg["Destination"]["delay"] = dest_delay

    def augment_trips(self):
        for trip in self.trips:
            trip["duration"] = trip["duration"].replace("PT", "").replace("M", "")
            for leg in trip["LegList"]["Leg"]:
                self.prepare_delay_info(leg)
                self.prepare_station_names(leg)
                self.prepare_times(leg)
                # Fix time
                leg["name"] = leg["name"].strip()

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
