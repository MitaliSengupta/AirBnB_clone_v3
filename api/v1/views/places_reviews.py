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
    for rev in place_obj.reviews:
        rev_obj.append(rev.to_dict())
    return jsonify(rev_obj)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def indv_review(review_id):
    """ Retrieves a Review object """
    review_obj = storage.get('Review', review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_dict)


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
    req = request.get_json()
    place_obj = storage.get('Place', place_id)
    user_obj = storage.get('User', req['user_id'])
    if place_obj is None:
        abort(404)
    if req is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in req:
        return jsonify({"error": "Missing user_id"}), 400
    if user_obj is None:
        abort(404)
    if 'text' not in req:
        return jsonify({"error": "Missing text"}), 400
    else:
        ruid = req["user_id"]
        rxt = req["text"]
        rev = Review(user_id=ruid, text=rxt, place_id=place_id)
        for key, value in req.items():
            setattr(rev, key, value)
        rev.save()
        return jsonify(rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    rev_obj = storage.get('Review', review_id)
    req = request.get_json()
    if not rev_obj:
        abort(404)
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    for key, val in req.items():
        if key not in [
            'id',
            'created_at',
            'user_id',
            'place_id',
                'updated_at']:
            setattr(rev_obj, key, val)
    rev_obj.save()
    return (jsonify(rev_obj.to_dict()), 200)
