from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from app.models.user import User
from .errors import unauthorized, forbidden
from . import api_blueprint_v1_0
from .service.user import verify_auth_token, generate_auth_token

# HTTPBasicAuth为flask 提供的基本用户登录验证系统，比flask_login更加基础，flask_login将用户信息存在
# 于session中，而HTTPBasicAuth则为无状态验证。
auth = HTTPBasicAuth()


@api_blueprint_v1_0.before_request
@auth.login_required
def before_request():
    """
    在每次请求前，判断用户携带了token或登录信息，而执行该函数需要login_required，login_required
    则会触发@auth.verify_password的回调函数。
    :return:
    """
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')

@auth.verify_password
def verify_password(email_or_token, password):
    """
    @auth.verify_password的回调函数，回调函数有多种，这里用了两个参数的回调函数。
    其他版本请咨询查找。
    当password为空时，说明用户携带了token访问，则需要验证token并从token中取出用户id；
    当password不为空是，说明用户准备使用密码登录，则从数据库中查找用户邮箱，并取出密码进行验证
    :param email_or_token: 即回调函数的username
    :param password:
    :return:
    """
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token.lower()).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api_blueprint_v1_0.route('/tokens/', methods=['POST'])
def get_token():
    """
    用于用户获取token
    :return:
    """
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': generate_auth_token(g.current_user,
        expiration=3600), 'expiration': 3600})

