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
    hbnb_api_host = getenv('HBNB_API_HOST', '0.0.0.0')
    hbnb_api_port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=hbnb_api_host, port=hbnb_api_port)
