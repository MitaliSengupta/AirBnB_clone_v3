#!/usr/bin/env python3
"""
App basis
"""
from flask import Flask, Blueprint,  make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})

@app.teardown_appcontext
def teardown(error):
    """ closes down current session """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
       a handler for 404 errors that returns a
       JSON-formatted 404 status code response
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    hosts = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)
