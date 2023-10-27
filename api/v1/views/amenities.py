#!/usr/bin/python3
"""
new view for Amenity objects that handles all
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

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """retrieves all Amenity instances"""
    amenities_dict = storage.all(Amenity)
    amenities_list = [obj.to_dict() for obj in amenities_dict.values()]
    return jsonify(amenities_list)

@app_views.route('/amenities/<id>', methods=['GET'], strict_slashes=False)
def get_amenity(id):
    """retrieves a amenity object based on id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(id):
    """deletes a amenity object based on id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a amenity object"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    inst = request.get_json()
    if 'name' not in inst:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**inst)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    """updates a amenity object based on id"""
    amenity = storage.get(Amenity, id)
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    attrs = request.get_json()
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    for k,v in attrs.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 201
    