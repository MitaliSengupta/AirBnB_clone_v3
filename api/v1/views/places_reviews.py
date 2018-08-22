#!/usr/bin/python3
""""
Review Module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, Blueprint
from models import storage, Review, Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id=None):
    """ Retrieves the list of all Review objects of a Place """
    place_obj = storage.get('Place', place_id)
    if not place_id or not place_obj:
        abort(404)
    else:
        rev_obj = []
        for rev in place_obj.reviews:
            rev_obj.append(rev.to_dict())
    return jsonify(rev_obj)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def indv_review(review_id=None):
    """ Retrieves a Review object """
    review_obj = storage.get('Review', review_id)
    if not review_id:
        abort(404)
    if not review_obj:
        abort(404)
    else:
        return jsonify(review.to_dict)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id=None):
    """ Deletes a Review object """
    review_obj = storage.get('Review', review_id)
    if notreview_id:
        abort(404)
    if not review_obj:
        abort(404)
    else:
        storage.delete(review_obj)
        return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a Review """
    place_obj = storage.get('Place', place_id)
    req = request.get_json()
    if not place_obj:
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
def update_review(review_id=None):
    """ Updates a Review object """
    rev_obj = storage.get('Review', review_id)
    req = request.get_json()
    if not review_id or not rev_obj:
        abort(404)
    if req is None:
        abort(400, 'Not a JSON')
    for key, val in req.items():
        if key not in 'id' and key not in 'created_at' and key not in 'user_id'\
           and key not in 'place_id' and key not in 'updated_at':
            setattr(rev_obj, key, val)
    rev_obj.save()
    return (jsonify(rev_obj.to_dict()), 200)
