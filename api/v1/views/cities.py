#!/usr/bin/python3
"""new view for City objects that handles all
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


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
def list_cities(state_id):
    """retrieves all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    cities_list = [city.to_dict() for city in state.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """retrieves a city object based on id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city object based on id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city object based on State's id"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    inst = request.get_json()
    if 'name' not in inst:
        return jsonify({"error": "Missing name"}), 400
    inst["state_id"] = state_id
    city = City(**inst)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<id>', methods=['PUT'], strict_slashes=False)
def update_city(id):
    """updates a city object based on id"""
    city = storage.get(City, id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    attrs = request.get_json()
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in attrs.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 201
