from flask import render_template, request, jsonify
from . import error_blueprint


@error_blueprint.app_errorhandler(403)
def forbidden(e):
    """
    当发生403错误无访问权限的时候调用的函数
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@error_blueprint.app_errorhandler(404)
def page_not_found(e):
    """
    当发生404错误的时候调用的函数
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@error_blueprint.app_errorhandler(500)
def internal_server_error(e):
    """
    当发生500服务器内部错误的时候调用的函数
    :param e:
    :return:
    """
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
