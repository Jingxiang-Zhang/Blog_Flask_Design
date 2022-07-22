from flask import jsonify, request, g, url_for, current_app, abort
from app import db
from app.models.post import Post
from app.models.role import Permission
from app.controller.api.v1_0 import api_blueprint_v1_0
from app.controller.api.v1_0.decorators import permission_required
from app.controller.api.v1_0.errors import forbidden
from ..service.post import post_info_to_json, from_json

@api_blueprint_v1_0.route('/posts/')
def get_posts():
    """
    获取数据库全部的posts发言，表示分页页码
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api/v1.0.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api/v1.0.get_posts', page=page+1)
    return jsonify({
        'posts': [post_info_to_json(post) for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api_blueprint_v1_0.route('/posts/<int:id>')
def get_post(id):
    """
    获取某一条发言记录
    :param id: 发言的id编号
    :return:
    """
    post = Post.query.get_or_404(id)
    return jsonify(post_info_to_json(post))


@api_blueprint_v1_0.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    """
    填写一条发言posts，评论格式为：
    post请求:
    res = requests.post("http://token值:@服务器地址:服务器端口/api/v1.0/posts/",
                    json={"body":"待发表的post内容"})
    使用postman测试，1. 请发送json请求，在请求栏中的Body中选择raw，
                        下方框输入{"body":"待发表的post内容"}，
                    2. 选择JSON，不是Text，
                        或者选择Header，找到Content-Type，将后面的值改为 application/json，
                    3. 将Header中的Accept值改为application/json
                        （这步用于 /app/controller/errors.py 中对于请求类型的判断
    :return:
    """
    post = None
    try:
        post = from_json(request.json)
    except Exception as e:
        abort(404)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post_info_to_json(post)), 201, \
        {'Location': url_for('api/v1.0.get_post', id=post.id)}


@api_blueprint_v1_0.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
    """
    修改一条评论，要求必须是评论作者才能修改，方法必须是PUT
    :param id: post的id
    :return:
    """
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post_info_to_json(post))
