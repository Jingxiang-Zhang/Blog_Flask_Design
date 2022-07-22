from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask_login import login_required, current_user

from . import user_blueprint
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, \
    CommentForm
from app import db
from app.models.role import Permission, Role
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.decorators import admin_required, permission_required
from flask import jsonify
import os
from PIL import Image
from hashlib import md5


@user_blueprint.route('/<username>')
def user(username):
    """
    用户界面跳转，获取用户发布的动态，并进行分页显示
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('routes/user/user.html', user=user, posts=posts,
                           pagination=pagination)


@user_blueprint.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    编辑个人信息页面
    :return:
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('user.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('routes/user/edit_profile.html', form=form)


@user_blueprint.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    """
    管理员编辑其他人信息
    :param id:
    :return:
    """
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('user.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('routes/user/edit_profile.html', form=form, user=user)


@user_blueprint.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    """
    点击某一条post后进行评论
    :param id:
    :return:
    """
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('user.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('routes/user/post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@user_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """
    编辑一条post评论
    :param id: 评论id
    :return:
    """
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('user.post', id=post.id))
    form.body.data = post.body
    return render_template('routes/user/edit_post.html', form=form)


@user_blueprint.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    """
    follow某个用户
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('user.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('user.user', username=username))


@user_blueprint.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    """
    取消关注
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('user.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('user.user', username=username))


@user_blueprint.route('/followers/<username>')
def followers(username):
    """
    查看自己关注的人的列表
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('routes/user/followers.html', user=user, title="Followers of",
                           endpoint='user.followers', pagination=pagination,
                           follows=follows)


@user_blueprint.route('/followed_by/<username>')
def followed_by(username):
    """
    查看关注自己的人的列表
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('routes/user/followers.html', user=user, title="Followed by",
                           endpoint='user.followed_by', pagination=pagination,
                           follows=follows)


@user_blueprint.route('/all')
@login_required
def show_all():
    """
    记录是否展示全部的人，如果这项设置了展示所有人的动态
    :return:
    """
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@user_blueprint.route('/followed')
@login_required
def show_followed():
    """
    记录是否展示全部的人，如果这项设置了则只会展示关注者的列表
    :return:
    """
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@user_blueprint.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    """
    用于修改评论
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('routes/user/moderate.html', comments=comments,
                           pagination=pagination, page=page)


@user_blueprint.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    """
    用于启用评论
    :param id:
    :return:
    """
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('user.moderate', page=request.args.get('page', 1, type=int)))


@user_blueprint.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    """
    用于关闭评论
    :param id:
    :return:
    """
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('user.moderate', page=request.args.get('page', 1, type=int)))


@user_blueprint.route('/avatar', methods=['POST'])
def avatar():
    """
    获取用户头像数据
    :return:
    """
    # 获取用户avatar的哈希值
    id = request.form["id"]
    user = User.query.get_or_404(id)

    import base64
    try:
        avatar_hash = user.avatar_hash

        # 获取avatar的根地址
        app = current_app._get_current_object()
        base = app.config['AVATAR_PATH']
        base_img = os.path.join(base, "avatar")
        # 取出前两位组成地址
        file_dir_base = os.path.join(base_img, avatar_hash[:2])
        file_dir = os.path.join(file_dir_base, avatar_hash)
        with open(file_dir + ".png", 'rb') as img_f:
            img_stream = img_f.read()
            img_stream = str(base64.b64encode(img_stream), 'utf-8')
    except:
        return jsonify({"data": url_for("static", filename='img/userprofile/default_avatar.png')})
    return jsonify({"data": "data:image/png;base64," + img_stream})


@user_blueprint.route('/upload_avatar', methods=['GET', 'POST'])
@login_required
def upload_avatar():
    """
    获取用户上传的头像
    """
    file = request.files.get('file')
    stream = file.stream
    if not file:
        abort(403)
    # 获取服务器初始化参数
    app = current_app._get_current_object()
    base = app.config['AVATAR_PATH']
    height = app.config['AVATAR_HEIGHT']
    width = app.config['AVATAR_WIDTH']
    min_height = app.config['AVATAR_MIN_HEIGHT']
    min_width = app.config['AVATAR_MIN_WIDTH']

    # 获取图像的比特流，一定要在Image打开之前获取，否则对象将被删除
    img_binary = stream.read()
    # Image读取数据
    img = Image.open(stream)
    # 计算图像缩放后的结果
    img.thumbnail((height, width))
    # 计算图像的哈希值
    img_hash = md5(img_binary).hexdigest()
    # 取出哈希值前2位，即前8比特，用来创建文件夹，进行分流
    base_img = os.path.join(base, "avatar")
    if not os.path.exists(base_img):
        os.mkdir(base_img)
    file_dir_base = os.path.join(base_img, img_hash[:2])
    if not os.path.exists(file_dir_base):
        os.mkdir(file_dir_base)
    img.save(os.path.join(file_dir_base, img_hash + ".png"))

    # 计算图像的缩略图
    img.thumbnail((min_height, min_width))
    base_min_img = os.path.join(base, "min_avatar")
    if not os.path.exists(base_min_img):
        os.mkdir(base_min_img)
    file_dir_base = os.path.join(base_min_img, img_hash[:2])
    if not os.path.exists(file_dir_base):
        os.mkdir(file_dir_base)
    img.save(os.path.join(file_dir_base, img_hash + ".png"))

    current_user.avatar_hash = img_hash
    db.session.add(current_user._get_current_object())
    db.session.commit()
    # photos.save(request.files['file'], 'pic.png')  # 保存图片
    return jsonify()


@user_blueprint.route('/get_batch_avatar', methods=['GET', 'POST'])
def get_batch_avatar():
    avatar_hash_list = request.form["avatar_hash_list"]
    avatar_hash_list = str(avatar_hash_list).split(";")

    app = current_app._get_current_object()
    base = app.config['AVATAR_PATH']
    base = os.path.join(base, "min_avatar")

    import base64
    avatar_list = list()
    for avatar_hash in avatar_hash_list:
        # 取出前两位组成地址
        file_dir_base = os.path.join(base, avatar_hash[:2])
        file_dir = os.path.join(file_dir_base, avatar_hash)
        try:
            with open(file_dir + ".png", 'rb') as img_f:
                img_stream = img_f.read()
                img_stream = str(base64.b64encode(img_stream), 'utf-8')
                avatar_list.append("data:image/png;base64," + img_stream)
        except Exception as e:
            avatar_list.append(url_for("static", filename='img/userprofile/default_avatar.png'))
    return jsonify(dict(data=avatar_list))
