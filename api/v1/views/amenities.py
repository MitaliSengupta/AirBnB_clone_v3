#!/usr/bin/python3
"""Create Amenity objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import Amenity


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def all_amenities():
    """
    gets all amenities
    """
    amenities = []
    for v in storage.all("Amenity").values():
        amenities.append(v.to_dict())
    return (jsonify(amenities))


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    getting amenity using an id
    """
    try:
        return (jsonify(storage.get("Amenity", amenity_id).to_dict()))
    except Exception:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"]
                 ,strict_slashes=False)
def delete_amenity(amenity_id):
    """
    deleting amenity based on id
    """
    try:
        storage.delete(storage.get("Amenity", amenity_id))
        storage.save()
        return (jsonify({}), 200)
    except Exception:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def post_amenity():
    """
    creates a new amenity
    """
    if not request.json:
        return (jsonify({"error": "Not a JSON"}), 400)
    amenity = request.get_json()
    if "name" not in amenity:
        return (jsonify({"error": "Missing name"}), 400)
    else:
        name = amenity["name"]
        am = Amenity(name=a_name)
        for key, value in amenity.items():
            setattr(ame, key, value)
        am.save()
        return (jsonify(am.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_am(amenity_id):
    """
    updates amenity
    """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    json = request.get_json()
    for key, value in json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
