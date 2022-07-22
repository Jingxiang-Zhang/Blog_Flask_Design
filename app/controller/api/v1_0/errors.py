from flask import jsonify
from app.exceptions import ValidationError
from app.controller.api.v1_0 import api_blueprint_v1_0


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api_blueprint_v1_0.errorhandler(404)
def url_not_found(e):
    response = jsonify({'error': 'url not found'})
    response.status_code = 404
    return response


@api_blueprint_v1_0.errorhandler(500)
def internal_error(e):
    response = jsonify({'error': 'server internal error'})
    response.status_code = 500
    return response


@api_blueprint_v1_0.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
