from flask import jsonify, request, url_for, abort
from app.api import bp
from app.api.errors import bad_request


@bp.route('/artifact/<object_id>', methods=['GET'])
def get_artifact(object_id):
    try:
        with open('artifacts/' + object_id+'.json', 'r') as f:
            artifact = f.read()
    except OSError as err:
        return bad_request(f'No artifact found with objectID: {object_id}')
    else:
        return jsonify(artifact)


