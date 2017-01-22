from flask import Flask, render_template
from simple_vbb.vbb import Vbb

app = Flask(__name__)
vbb = Vbb()

FROM = "S Nikolassee"

FROM = "S Wannsee"
TO = "U Stadtmitte (Berlin)"
FROM_ID = vbb.get_station_ext_id(FROM)
TO_ID = vbb.get_station_ext_id(TO)


@app.route("/")
def root():
    text = vbb.get_trip(FROM_ID, TO_ID)
    return render_template("main.html", text=text)


@app.route("/trips")
def trips():
    trips = vbb.get_trip(FROM_ID, TO_ID)
    return render_template("trips.html", trips=trips)

if __name__ == "__main__":
    app.run()
