#!/usr/bin/python3
"""
This file contains the amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from models.place import Place
from models.amenity import Amenity

from os import getenv


db = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amens_of_place(place_id):
    """ list amenities in a place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if db == "db":
        list_as = [obj.to_dict() for obj in place.amenities]
    else:
        list_as = place.amenity_ids
    return jsonify(list_s)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amens_of_place(place_id, amenity_id):
    """ delete instance """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if db == "db":
        if amenity not in place.amenities:
            abort(404)
        else:
            place.amenities.remove(amenity)
    else:
        if amenity not in place.amenity_ids:
            abort(404)
        else:
            place.amenity_ids.remove(amenity_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_ameni_of_place(place_id, amenity_id):
    """ create amen of place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if db == "db":
        if amenity in place.amenities:
            return (jsonify(amenity.to_dict()), 200)
        else:
            place.amenitites.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return (jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict(), 201)
