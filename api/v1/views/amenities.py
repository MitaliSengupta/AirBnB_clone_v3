#!/usr/bin/python3
"""
Create a view for amenity objects that handles
all default RestFul api actions
"""
from flask import jsonify, abort, request
from models import storage
from models import Amenity
from models import State
from models import City
from api.v1.views import app_views


@app_views.route("/amenities/", methods=["GET"], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amen(amenity_id=None):
    """
    prints all amenities
    """
    if amenity_id is None:
        get_am = storage.all("Amenity")
        list_am = [value.to_dict() for key, value in get_am.items()]
        return (jsonify(list_am))
    list_am = storage.get("Amenity", amenity_id)
    if list_am is None:
        abort(404)
    return (jsonify(list_am.to_dict()))


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """
    deletes amenity based on id
    """
    del_am = storage.all("Amenity").values()
    obj = [obje.to_dict() for obje in del_am if obje.id == amenity_id]
    if obj is None:
        abort(404)
    obj.remove(obj[0])
    for obje in del_am:
        if obje.id == amenity_id:
            storage.delete(obje)
            storage.save()
    return (jsonify({}), 200)


