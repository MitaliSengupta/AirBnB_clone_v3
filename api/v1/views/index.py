#!/usr/bin/python3
"""
creating api file
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """
    return status in json
    """
    stat = {"status" : "OK"}
    return (jsonify(stat))
