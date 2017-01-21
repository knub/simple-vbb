from flask import Flask
from flask import render_template
from simple_vbb.vbb import Vbb

app = Flask(__name__)
vbb = Vbb()


@app.route("/")
def root():
    return render_template("main.html")

if __name__ == "__main__":
    app.run()
