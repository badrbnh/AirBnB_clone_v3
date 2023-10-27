#!/usr/bin/python3
"""new view for Review objects that handles all
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

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def list_reviews(place_id):
    """retrieves all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """retrieves a review object based on id"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """deletes a review object based on id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Not found"}), 404

@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """creates a review object based on Place's id"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    inst = request.get_json()
    if 'user_id' not in inst:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, inst["user_id"])
    if not user:
        return jsonify({"error": "Not found"}), 404
    if 'text' not in inst:
        return jsonify({"error": "Missing text"}), 400
    inst["place_id"] = place_id 
    review = Review(**inst)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<id>', methods=['PUT'], strict_slashes=False)
def update_review(id):
    """updates a Review object based on id"""
    review = storage.get(Review, id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    attrs = request.get_json()
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    for k,v in attrs.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 201
    