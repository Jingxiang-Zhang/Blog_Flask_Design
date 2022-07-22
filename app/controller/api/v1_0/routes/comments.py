from flask import jsonify, request, g, url_for, current_app, abort
from app import db
from app.models.post import Post
from app.models.role import Permission
from app.models.comment import Comment
from app.controller.api.v1_0 import api_blueprint_v1_0
from app.controller.api.v1_0.decorators import permission_required
from ..service.comment import comment_info_to_json, from_json


@api_blueprint_v1_0.route('/comments/')
def get_comments():
    """
    获取全部评论，可用url拼接的方式提供参数page，表示分页页码
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api/v1.0.get_comments', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api/v1.0.get_comments', page=page + 1)
    return jsonify({
        'comments': [comment_info_to_json(comment) for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api_blueprint_v1_0.route('/comments/<int:id>')
def get_comment(id):
    """
    获取某一条评论记录
    :param id: 发言的id编号
    :return:
    """
    comment = Comment.query.get_or_404(id)
    return jsonify(comment_info_to_json(comment))


@api_blueprint_v1_0.route('/posts/<int:id>/comments/')
def get_post_comments(id):
    """
    获取某id的post中的全部comments
    :param id: post的id
    :return:
    """
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api/v1.0.get_post_comments', id=id, page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api/v1.0.get_post_comments', id=id, page=page + 1)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api_blueprint_v1_0.route('/posts/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_post_comment(id):
    """
    填写一条评论，需要提供posts的id，评论格式为：
    post请求:
    res = requests.post("http://token值:@服务器地址:服务器端口/api/v1.0/posts/posts的id值/comments/",
                    json={"body":"待发表的post内容"})
    使用postman测试，1. 请发送json请求，在请求栏中的Body中选择raw，
                        下方框输入{"body":"待发表的post内容"}，
                    2. 选择JSON，不是Text，
                        或者选择Header，找到Content-Type，将后面的值改为 application/json，
                    3. 将Header中的Accept值改为application/json
                        （这步用于 /app/controller/errors.py 中对于请求类型的判断
    :return:
    """
    comment = None
    post = Post.query.get_or_404(id)
    try:
        comment = from_json(request.json)
    except Exception as e:
        abort(404)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, \
           {'Location': url_for('api/v1.0.get_comment', id=comment.id)}
