#!/usr/bin/python3
"""
new view for User objects that handles all
default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def list_users():
    """retrieves all User instances"""
    users_dict = storage.all(User)
    users_list = [obj.to_dict() for obj in users_dict.values()]
    return jsonify(users_list)


@app_views.route('/users/<id>', methods=['GET'], strict_slashes=False)
def get_user(id):
    """retrieves a user object based on id"""
    user = storage.get(User, id)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def delete_user(id):
    """deletes a user object based on id"""
    user = storage.get(User, id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates a user object"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    inst = request.get_json()
    if 'email' not in inst:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in inst:
        return jsonify({"error": "Missing password"}), 400
    user = User(**inst)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    """updates a user object based on id"""
    user = storage.get(User, id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    attrs = request.get_json()
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in attrs.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
