from flask import url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app.models.user import User


def user_info_to_json(user):
    """
    用于api接口，返回josn格式的用户数据，其中不返回邮箱
    :return:
    """
    json_user = {
        'url': url_for('api/v1.0.get_user', id=user.id),
        'username': user.username,
        'member_since': user.member_since,
        'last_seen': user.last_seen,
        'posts_url': url_for('api/v1.0.get_user_posts', id=user.id),
        'followed_posts_url': url_for('api/v1.0.get_user_followed_posts',
                                      id=user.id),
        'post_count': user.posts.count()
    }
    return json_user


def generate_auth_token(user, expiration):
    """
    用于api接口，因为是无状态访问，因此每次用户访问需要携带token
    :param expiration:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({'id': user.id}).decode('utf-8')


def verify_auth_token(token):
    """
    用于检验用户token，从token中取出用户id并进行检验
    :param token:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return None
    return User.query.get(data['id'])
