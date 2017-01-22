from flask import Flask, render_template
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


def augment_trip(trips):
    for trip in trips:
        trip["duration"] = trip["duration"].replace("PT", "").replace("M", "")
        for leg in trip["LegList"]["Leg"]:
            leg["name"] = leg["name"].replace("Bus ", "B").strip()
    return trips


@app.route("/")
def root():
    text = vbb.get_trip(FROM_ID, TO_ID)
    return render_template("main.html", text=text)


@app.route("/trips")
def trips():
    trips = augment_trip(vbb.get_trip(FROM_ID, TO_ID))
    return render_template("trips.html", trips=trips, from_station=FROM, to_station=TO)

if __name__ == "__main__":
    app.run()
