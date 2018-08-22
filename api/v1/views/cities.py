#!/usr/bin/python3
"""
Creating new view for State object
that handles all default RestFul API actions
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def state_city(state_id):
    """
    function to retrieve list of all cities connected to states
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    all_cities = storage.all("City")
    for k, v in all_cities.items():
        if v.state_id == str(state_id):
            cities.append(v.to_dict())
    return (jsonify(cities))


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def city_all(city_id):
    """
    get cities by id
    """
    try:
        ct = storage.get("City", city_id)
        return (jsonify(ct.to_dict()))
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_cities(city_id):
    """
    function to delete city based on id
    """
    city = storage.get('City', city_id)
    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def post_cities(state_id):
    """
    function to create a city
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if not content:
        return (jsonify({"error": "Not a JSON"}), 400)
    if "name" not in content:
        return (jsonify({"error": "Missing name"}), 400)
    content['state_id'] = state.id
    post_city = City(**content)
    post_city.save()

    return (jsonify(post_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_cities(city_id):
    """
    function to update City
    """
    set_city = storage.get("City", city_id)
    if set_city is None:
        abort(404)
    if not request.json():
        return (jsonify({"error": "Not a JSON"}), 400)
    content = request.get_json()
    for k, v in content.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(set_city, k,v )
    set_city.save()
    return (jsonify(set_city.to_dict()), 200)
