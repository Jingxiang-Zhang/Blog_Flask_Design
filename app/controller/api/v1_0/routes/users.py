from flask import jsonify, request, current_app, url_for
from app.controller.api.v1_0 import api_blueprint_v1_0
from app.models.user import User
from app.models.post import Post
from ..service.user import user_info_to_json
from ..service.post import post_info_to_json


@api_blueprint_v1_0.route('/users/<int:id>')
def get_user(id):
    """
    获取用户信息
    :param id: 用户id
    :return: json结构的用户信息
    """
    user = User.query.get_or_404(id)
    return jsonify(user_info_to_json(user))


@api_blueprint_v1_0.route('/users/<int:id>/posts/')
def get_user_posts(id):
    """
    获取用户的所有post
    :param id: 用户id
    :return: json结构的用户发表的全部posts
    """
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api/v1.0.get_user_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api/v1.0.get_user_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post_info_to_json(post) for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api_blueprint_v1_0.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    """
    获取用户关注的人的全部发言
    :param id: 该用户id
    :return:
    """
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api/v1.0.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api/v1.0.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post_info_to_json(post) for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
