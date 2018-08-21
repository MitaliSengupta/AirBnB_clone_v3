#!/usr/bin/python3
"""
Creating new view for State object
that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import State
from models import City


app = Flask(__name__)


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def state_city(state_id):
    """
    function to retrieve list of all cities connected to states
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = state.cities
    get_cities = [city.to_dict() for city in cities]
    return (jsonify(get_cities))


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city(city_id):
    """
    get cities by id
    """
    ct = storage.get("City", city_id)
    if ct is None:
        abort(404)
    return (jsonify(ct.to_dict()))


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_cities(cities_id):
    """
    function to delete city based on id
    """
    del_city = storage.all("City").values()
    obj = [obje.to_dict() for obje in del_city if obje.id == city_id]
    if obj == []:
        abort(404)
    obj.remove(obj[0])
    for obje in del_city:
        if obje.id == city_id:
            storage.delete(obje)
            storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"], strict_slashes=False)
def post_cities(state_id):
    """
    function to create a city
    """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    name = content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    add_city = City()
    add_city.state_id = state_id
    add_city.name = name
    add_city.save()

    return (jsonify(add_city.to_dict()), 201)


@app_views.route('/city/<city_id>', methods=["PUT"], strict_slashes=False)
def update_cities(city_id):
    """
    function to update City
    """
    content = request.get_json()
    if content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    set_city = storage.get("City", city_id)
    if set_city is None:
        abort(404)

    for key, value in content.items():
        if key != "id" or key != "created_at" or key != "updated_at" or key != "state_id":
            setattr(set_city, key, value)

    set_city.save()
    return jsonify(set_city.to_dict())
