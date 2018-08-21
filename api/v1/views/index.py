#!/usr/bin/env python3
"""
an endpoint that retrieves the number of each objects by type
"""
from flask import jsonify, Blueprint
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """
    return status in json
    """
    stat = {"status": "OK"}
    return (jsonify(stat))


@app_views.route("/stats")
def stats():
    """
    endpoint that retrieves number of obj by type
    """
    stat = {"amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")}
    return (jsonify(stat))
