#!/usr/bin/env python3
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
    return jsonify(users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def indv_user():
    """ Retrieves a User object """
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user():
    """ Deletes a User object """
    user = storage.all('User').value()
    if user is None:
        abort(404)
    for erase in user:
        if erase.id == user_id:
            storage.delete(user)
            return (jsonify({}), 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    req = request.get_json()
    if req is None:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in req:
        return (jsonify({'error': 'Missing email'}), 400)
    if 'password' not in req:
        return (jsonify({'error': 'Missing password'}), 400)
    if 'email' in req and 'password' in req:
        new_user = User()
        for key, value in req.items():
            setattr(new_user, key, value)
        new_user.save()
        return (jsonify(new_user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user():
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
