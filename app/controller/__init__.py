from .main import main_blueprint
from .auth import auth_blueprint
from app.controller.api import api_blueprint_v1_0
from .user import user_blueprint

from flask_sqlalchemy import get_debug_queries
from flask import Blueprint, current_app, abort, request

error_blueprint = Blueprint('error', __name__)

from . import errors
from app.models.role import Permission

__all__ = ['api_blueprint_v1_0',

           'main_blueprint',
           'auth_blueprint',
           'error_blueprint',
           'user_blueprint']


@error_blueprint.app_context_processor
def inject_permissions():
    """
    添加整个范围的参数
    :return:
    """
    return dict(Permission=Permission)


@main_blueprint.after_app_request
def after_request(response):
    """
    在完成每一次请求的时候，进行判断，数据库连接是否超时
    :param response:
    :return:
    """
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


# ---------------- 停止使用的函数 -----------------------

@main_blueprint.route('/shutdown')
def server_shutdown():
    """
    该函数目前不使用，用于前台关闭后台的服务器
    :return:
    """
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
