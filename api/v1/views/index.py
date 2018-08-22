#!/usr/bin/python3
"""
an endpoint that retrieves the number of each objects by type
"""
from flask import jsonify
from models import classes
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
    dic = {}
    for cls in classes:
        dic[cls] = storage.count(classes[cls])
    return (jsonify(dic))
