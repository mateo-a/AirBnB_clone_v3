#!/usr/bin/python3
""" Places reviews """
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def review_by_id(place_id):
    """ List al reviws in a place id """
    rev = []
    if itm_locator(place_id, 'Place') is False:
        abort(404)
    place = storage.all('Review')
    if place:
        for key, value in place.items():
            if value.to_dict()['place_id'] == place_id:
                rev.append(value.to_dict())
        return jsonify(rev)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def review_object(review_id):
    """ all review of and object """
    rev = storage.get("Review", review_id)
    if rev:
        return jsonify(rev.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete an object eith ther ID"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create a new review object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, 'Not a JSON')
    if "user_id" not in kwargs:
        abort(400, 'Missing user_id')
    elif itm_locator(kwargs['user_id'], 'User') is False:
        abort(404)
    if "text" not in kwargs:
        abort(400, 'Missing text')
    kwargs['place_id'] = place_id
    review = Review(**kwargs)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ Update review object method """
    ignore_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, 'Not a JSON')
    for key, val in kwargs.items():
        if key not in ignore_list:
            setattr(review, key, val)
    review.save()
    return jsonify(review.to_dict()), 200


def itm_locator(id, item):
    """ find into items list """
    list_items = storage.all(str(item)).items()
    for key, value in list_items:
        if value.to_dict()['id'] == id:
            return True
    return False
