from flask import render_template, redirect, url_for, request, current_app
from flask_login import current_user
from . import main_blueprint
from .forms import PostForm
from app import db
from app.models.role import Permission
from app.models.post import Post


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """
    首页函数，用于用户发布动态
    :return:
    """
    form = PostForm()
    # 提交表单后会自动提交到这个网址下，根据validate_on_submit判断是否是该表单，然后进行相关的判断与跳转
    # 其中一个优点是，避免用户刷新的时候浏览器出现重复提交form的提醒
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))

    # 获取分页
    page = request.args.get('page', 1, type=int)

    # 一个开关，判断用户是否只查看关注者的动态
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts  # 返回一个查询，只有关注者的动态
    else:
        query = Post.query  # 返回全部查询
    # 使用paginate进行分页
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)
