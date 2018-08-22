#!/usr/bin/python3
"""
User Module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_user():
    """ Retrieves the list of all User objects """
    usr_obj = []
    users = storage.all('User').values()
    for user in users:
        usr_obj.append(user.to_dict())
    return (jsonify(usr_obj), 200)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def indv_user(user_id=None):
    """ Retrieves a User object """
    user = storage.get('User', user_id)
    if user:
        return (jsonify(user.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    try:
        del_user = storage.all("User").values()
        obj = [obje.to_dict() for obje in del_city if obje.id == user_id]
        if obj is None:
            abort(404)
        obj.remove(obj[0])
        for obje in del_user:
            if obje.id == user_id:
                storage.delete(obje)
                storage.save()
        return (jsonify({}), 200)
    except Exception:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user(user_id):
    """ Creates a User """
    req = request.get_json()
    usr_st = storage.get("User", user_id)
    if usr_st is None:
        abort(404)
    if req is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in req:
        return (jsonify({'error': 'Missing email'}), 400)
    if 'password' not in req:
        return (jsonify({'error': 'Missing password'}), 400)
    if 'email' in req and 'password' in req:
        content['user_id'] = user.id
        post_user = User(**req)
        post_user.save()
        return (jsonify(post_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """ Updates a User object """
    req = request.get_json()
    if req is None:
        return (jsonify({'error': "Not a JSON"}), 400)
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    for key, value in req.iterms():
        if key not in 'id' and key not in 'created_at' and\
                key not in 'updated_at' and key not in 'email':
            setattr(user_obj, key, value)
    user_obj.save()
    return (jsonify(user_obj.to_dict()), 200)
