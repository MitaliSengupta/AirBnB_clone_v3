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
    if place_id is None or place_obj is None:
        abort(404)
    else:
        rev_obj = []
        for rev in place_obj.reviews:
            rev_obj.append(rev.to_dict())
    return jsonify(rev_obj)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def indv_review(review_id):
    """ Retrieves a Review object """
    review_obj = storage.get('Review', review_id)
    if review_id is None or review_obj is None:
        abort(404)
    if review_obj:
        return jsonify(review.to_dict)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """ Deletes a Review object """
    try:
        storage.delete(storage.get("Review", review_id))
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review """
    place_obj = storage.get('Place', place_id)
    req = request.get_json()
    if place_obj is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req:
        abort(400, 'Missing user_id')
    if 'text' not in req:
        abort(400, 'Missing text')
    req['place_id'] = place_id
    new_rev = Review(**req)
    new_rev.save()
    return (jsonify(new_rev.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    rev_obj = storage.get('Review', review_id)
    req = request.get_json()
    if review_id is None or rev_obj is None:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')
    for key, val in req.items():
        if key not in 'id' and key not in 'created_at' and key not in 'user_id'\
           and key not in 'place_id' and key not in 'updated_at':
            setattr(rev_obj, key, val)
    rev_obj.save()
    return (jsonify(rev_obj.to_dict()), 200)
