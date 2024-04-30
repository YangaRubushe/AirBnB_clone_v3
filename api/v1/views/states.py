#!/usr/bin/python3
"""View for State"""
from models import storage
from api.v1.views import app_views
from models.state import State
from flask import jsonify, request, abort, make_response


@app_views.route('/states', strict_slashes=False, methods=["GET", "POST"])
def get_states():
    """Get or create a states"""
    states = storage.all("State")

    if request.method == "GET":
        return jsonify([obj.to_dict() for obj in states.values()])

    if request.method == "POST":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if request.get_json().get("name") is None:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        state = State(**request.get_json())
        state.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def get_state_id(state_id=None):
    """Get all states"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # Get all states
    if request.method == "GET":
        return jsonify(state.to_dict())
    # Crate a state
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, val in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, val)
        state.save()
        return jsonify(state.to_dict())
    # DELETE A STATES OBJ
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({})
