#!/usr/bin/python3
"""new view for Place objects that handles all
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

@app_views.route('cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def list_places(city_id):
    """retrieves all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """retrieves a place object based on id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """deletes a Place object based on id"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """creates a Place object based on City's id"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    inst = request.get_json()
    if 'user_id' not in inst:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, inst["user_id"])
    if not user:
        return jsonify({"error": "Not found"}), 404
    if 'name' not in inst:
        return jsonify({"error": "Missing name"}), 400
    inst["city_id"] = city_id 
    place = Place(**inst)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201

@app_views.route('/places/<id>', methods=['PUT'], strict_slashes=False)
def update_place(id):
    """updates a Place object based on id"""
    place = storage.get(Place, id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    attrs = request.get_json()
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    for k,v in attrs.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 201
    