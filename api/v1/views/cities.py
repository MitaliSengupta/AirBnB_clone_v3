#!/usr/bin/python3
'''
   This module handles all default RestFul API actions for City objects.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities_by_state(state_id):
    '''
       Retrieves all City objects from storage that belong to specified State
    '''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities_list = []
    cities = storage.all("City")
    for k, v in cities.items():
        if v.state_id == str(state_id):
            cities_list.append(v.to_dict())

    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_by_id(city_id):
    '''
       Retrieves a specified City object from storage
    '''
    try:
        city = storage.get("City", city_id)
        format_city = city.to_dict()
        return jsonify(format_city)
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    '''
       Deletes a specified City object from storage
    '''
    try:
        city = storage.get("City", city_id)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''
       Creates a new City object and saves it to storage
    '''
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        city_dict = request.get_json()
        if "name" in city_dict:
            city_name = city_dict["name"]
            city = City(name=city_name, state_id=state_id)
            for k, v in city_dict.items():
                setattr(city, k, v)
            city.save()
        else:
            return jsonify({"error": "Missing name"}), 400
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    '''
       Updates an existing City object and saves it to storage
    '''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    req = request.get_json()
    for k, v in req.items():
        if k is not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, k, v)
    city.save()

    return jsonify(city.to_dict()), 200
