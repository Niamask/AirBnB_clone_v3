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


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ get reviews by place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ get review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """ delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_obj_review(place_id):
    """ create new instance """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return abort(400, "Not a JSON")
    if 'user_id' not in request.get_json():
        return abort(400, "Missing user_id")
    if 'text' not in request.get_json():
        return abort(400, "Missing text")
    kwargs = request.get_json()
    kwargs['place_id'] = place_id
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        abort(404)
    obj = Review(place_id=place_id, **kwargs)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/review/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def post_review(review_id):
    """ update review  """
    if not request.get_json():
        return abort(400, "Not a JSON")
    obj = storage.get(Review, user_id)
    if obj is None:
        abort(404)
    for ke, value in request.get_json().items():
        if ke not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(obj, ke, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
