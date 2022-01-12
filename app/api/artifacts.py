from flask import jsonify, request, url_for, abort
from app.api import bp
from app.api.errors import bad_request

import os
import json

artifact_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'artifacts/')


@bp.route('/artifact/<object_id>', methods=['GET'])
def get_artifact(object_id):
    try:
        with open(artifact_dir + object_id + '.json', 'r') as f:
            artifact = f.read()
    except OSError as err:
        return bad_request(f'No artifact found with objectID: {object_id}')
    else:
        return jsonify({object_id: artifact})


@bp.route('artifact/<object_id>', methods=['POST'])
def create_artifact(object_id):
    artifact = request.get_json() or {}
    if os.path.isfile(os.path.join(artifact_dir, object_id+ '.json')):
        return bad_request(f'Artifact with objectID: {object_id} already exists. Cannot create resource.')
    else:
        try:
            with open(artifact_dir + object_id + '.json', 'wb') as file:
                file.write(json.dumps(artifact).encode())
        except OSError as err:
            return bad_request(f'Something went wrong, please try again')
        else:
            response = jsonify({object_id: artifact})
            response.status_code = 201
            return response

