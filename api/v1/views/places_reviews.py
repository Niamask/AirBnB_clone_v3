#!/usr/bin/python3
"""
This file contains the User module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from models.place import Place
from models.review import Review
from flasgger.utils import swag_from


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/review/get.yml', methods=['GET'])
def get_all_reviews(place_id):
    """ get reviews by place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/review/get_id.yml', methods=['GET'])
def get_review(review_id):
    """ get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/review/delete.yml', methods=['DELETE'])
def del_review(review_id):
    """ delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/review/post.yml', methods=['POST'])
def create_obj_review(place_id):
    """ create new instance """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    kwargs = request.get_json()
    kwargs['place_id'] = place_id
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    obj = Review(**kwargs)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/review/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/review/put.yml', methods=['PUT'])
def post_review(review_id):
    """ update review  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Review, user_id)
    if obj is None:
        abort(404)
    for ke, value in request.get_json().items():
        if ke not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(obj, ke, value)
    obj.save()
    return jsonify(obj.to_dict())
