from datetime import datetime
from flask import Flask, render_template
import re
import sys

from simple_vbb.vbb import Vbb, DummyVbb, AccessKeyMissingException

app = Flask(__name__)

str_to_ext_id_cache = {}


def resolve_station(search_str):
    if search_str in str_to_ext_id_cache:
        return str_to_ext_id_cache[search_str]
    else:
        ext_id = vbb.get_station_ext_id(search_str)
        str_to_ext_id_cache[search_str] = ext_id
        return ext_id


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
            duration = trip["duration"]
            duration = duration.replace("PT", "")
            if "H" in duration:
                h_index = duration.index("H")
                m_index = duration.index("M")
                hours = duration[:h_index]
                minutes = int(duration[h_index + 1:m_index])
                trip["duration"] = "%s:%02d" % (hours, minutes)
            else:
                minutes = int(duration.replace("M", ""))
                trip["duration"] = "0:%02d" % minutes
            for leg in trip["LegList"]["Leg"]:
                self.prepare_delay_info(leg)
                self.prepare_station_names(leg)
                self.prepare_times(leg)
                # Fix time
                leg["name"] = leg["name"].strip()

    def __iter__(self):
        return iter(self.trips)


@app.route("/<from_station>-to-<to_station>")
def fromto(from_station=None, to_station=None):
    from_id = resolve_station(from_station)
    to_id = resolve_station(to_station)
    trips = TripsViewModel(vbb.get_trip(from_id, to_id))
    return render_template("trips.html", trips=trips, from_station=from_station.title(), to_station=to_station.title())


if __name__ == "__main__":
    try:
        vbb = Vbb()
        # vbb = DummyVbb()
    except AccessKeyMissingException:
        print("Missing access_key.txt. Exiting.")
        sys.exit()

    app.run()
