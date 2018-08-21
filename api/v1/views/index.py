#!/usr/bin/python3
"""
creating api file
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    return status in json
    """
    stat = {"status" : "OK"}
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
