#!/usr/bin/python3
"""
Create new view for link b/w place and amenities objects that
handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import Place
from models import Amenity
import os


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def amenities_places(place_id):
    """
    retrieves all amenities by place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amen = place.amenities
        for amen in amenity:
            amenity.append(amen.to_dict())
    else:
        place_amen = place.amenity_ids
        for am in place_amen:
            amenity.append(storage.get('Amenity', am).to_dict())
    return jsonify(amenity)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["DELETE"]
                 , strict_slashes=False)
def delete_obj(place_id, amenity_id):
    """
    Delete place amenity obj
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amen = place.amenities
        if am not in place_amen:
            abort(404)
        place_amen.remove(am)
    else:
        place_amen = place.amenity_ids
        if amenity_id not in place_amen:
            abort(404)
        place_amen.remove(amenity_id)
    place.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"]
                 , strict_slashes=False)
def post_pl_am(place_id, amenity_id):
    """
    link pl to amen
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amen = place.amenities
        if am in place_amen:
            return jsonify(am.to_dict()), 200
        place_amen.append(am)
    else:
        place_amen = place.amenity_ids
        if amenity_id in place_amen:
            return jsonify(am.to_dict()), 200
        place_amen.append(amenity_id)
    place.save()
    return jsonify(am.to_dict()), 201
