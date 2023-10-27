#!/usr/bin/python3
"""
new view for State objects that handles all
default RESTFul API actions
"""
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify, request
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """retrieves all state instances"""
    states_dict = storage.all(State)
    states_list = [obj.to_dict() for obj in states_dict.values()]
    return jsonify(states_list)

@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def get_state(id):
    """retrieves a state object based on id"""
    state = storage.get(State, id)
    if state:
        return jsonify(state.to_dict())
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def delete_state(id):
    """deletes a state object based on id"""
    state = storage.get(State, id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a state object"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    inst = request.get_json()
    if 'name' not in inst:
        return jsonify({"error": "Missing name"}), 400
    state = State(**inst)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def update_state(id):
    """updates a state object based on id"""
    state = storage.get(State, id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    attrs = request.get_json()
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    for k,v in attrs.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 201
    