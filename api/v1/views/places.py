#!/usr/bin/python3
"""
Place Module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, Place, City, User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_place(city_id):
    """ Retrieves the list of all Place objects of a City """
    places_obj = []
    city_obj = storage.get('City', city_id)
    if city_id:
        for city in city_obj.places:
            places_obj.append(city.to_dict())
    else:
        abort(404)
    return jsonify(places_obj)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def indv_place(place_id):
    """ Retrieves a Place object """
    place_obj = storage.get('Place', place_id)
    if place_obj is None or place_id is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id=None):
    """ Deletes a Place object """
    place_obj = storage.get('Place', place_id)
    if place_obj is None:
        abort(404)
    place_obj.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    req = request.get_json()
    city_obj = storage.get("City", city_id)
    user_obj = storage.get("User", data['user_id'])
    if req is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if city_obj is None:
        abort(404)
    if 'user_id' not in req:
        return (jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in req:
        return (jsonify({'error': 'Missing name'}), 400)
    if user_obj:
        req['city_id'] == city_id
        new_place = Place(**req)
        new_place.save()
        return (jsonify(new_place.to_dict()), 201)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    req = request.get_json()
    place_obj = storage.get("Place", place_id)
    if req is None:
        return (jsonify({'error': "Not a JSON"}), 400)
    if place_obj is None:
        abort(404)
    else:
        for key, val in req.items():
            if key not in 'id' and key not in 'created_at' and\
               key not in 'user_id' and key not in 'city_id':
                setattr(place_obj, key, val)
    place_obj.save()
    return (jsonify(my_place.to_dict()), 200)
