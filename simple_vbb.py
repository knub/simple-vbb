from flask import Flask
from simple_vbb.vbb import Vbb

app = Flask(__name__)
vbb = Vbb()


@app.route("/")
def root():
    return vbb.foo()

if __name__ == "__main__":
    app.run()
