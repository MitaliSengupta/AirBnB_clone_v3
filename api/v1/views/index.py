#!/usr/bin/env python3
"""
an endpoint that retrieves the number of each objects by type
"""
from flask import jsonify, Blueprint
from models import storage
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """ retrieves the status of a JSON file """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places":  storage.count("Place"),
        "reviews":  storage.count("Review"),
        "states":  storage.count("State"),
        "users": storage.count("User")
        })
