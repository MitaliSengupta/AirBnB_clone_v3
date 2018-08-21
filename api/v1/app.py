#!/usr/bin/python3
"""
creating a blueprint for flask
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    closes the current session
    """
    storage.close()


if __name__ == "__main__":
    hosts = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)
