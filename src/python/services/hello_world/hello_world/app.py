import time

from flask import Flask
import os

# using package from lessmore_test
from lessmore_test.clock import clock

clock.enable()
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/stats")
def stats():
    clock("time.sleep(1)")
    time.sleep(1)
    clock("time.sleep(1)")
    return str(clock.stats())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, host="0.0.0.0", port=port)
