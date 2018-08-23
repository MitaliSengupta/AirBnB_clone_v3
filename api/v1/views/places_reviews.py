#!/usr/bin/python3
""""
Review Module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, Blueprint
from models import storage, Review, Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place_obj = storage.get('Place', place_id)
    if place_id is None:
        abort(404)
    rev_obj = []
    rev_str = storage.all("Review").items()
    for key, value in rev_str:
        if value.place_id == place_id:
            rev_obj.append(value.to_dict())
    return jsonify(rev_obj)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def indv_review(review_id):
    """ Retrieves a Review object """
    try:
        rev_obj = storage.get("Review", review_id)
        return jsonify(rev_obj.to_dict())
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """ Deletes a Review object """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    review_obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    req = request.json
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    rev_req = request.get_json()
    if "user_id" not in rev_req:
        return jsonify({"error": "Missing user_id"}), 400
    user_obj = storage.get("User", rev_req["user_id"])
    if user_obj is None:
        abort(404)
    if "text" not in rev_req:
        return jsonify({"error": "Missing text"}), 400
    else:
        ruid = rev_req["user_id"]
        rxt = rev_req["text"]
        rev = Review(user_id=ruid, text=rxt, place_id=place_id)
        for key, value in rev_req.items():
            setattr(rev, key, value)
        rev.save()
        return jsonify(rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    rev_obj = storage.get('Review', review_id)
    if not rev_obj:
        abort(404)
    req = request.json()
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    rev_json = request.get_json()
    for key, val in rev_json.items():
        if key not in ['id', 'created_at', 'user_id',\
                       'place_id', 'updated_at']:
            setattr(rev_obj, key, val)
    rev_obj.save()
    return (jsonify(rev_obj.to_dict()), 200)
