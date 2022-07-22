from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from .. import db, login_manager
from .role import Role, Permission
from .post import Post


class Follow(db.Model):
    """
    多对多关系，user关注user，使用follow表存储
    """
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class AnonymousUser(AnonymousUserMixin):
    """
    定义匿名用户
    """

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login通过装饰器@login_required来检查访问视图函数的用户是否已登录，
    没有登录时会跳转到login_manager.login_view = 'auth.login'所注册的登录页。
    登录时即需调用login_user()函数，而在内部调用了由我们注册的回调函数。
    该写法是基本固定的
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False, comment="whether emile is confirmed")
    name = db.Column(db.String(64), comment="user real name")
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            # 初始化用户权限，设置为默认权限user
            self.role = Role.query.filter_by(default=True).first()
        # 让用户follow自己
        self.follow(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        每次调用该函数都会给密码加密
        :param password: 未加密的密码
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        检验密码
        :param password: 未加密的密码
        :return: 是否通过验证
        """
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        生成确认序列，附带用户id，用户注册生成邮箱验证使用
        :param expiration: 有效时间
        :return: 生成的序列
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        """
        给定一个token，判断是否合法，用户注册邮箱验证的时候使用
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        """
        生成密码重置的token，用于发送邮箱验证
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        """
        用于重置密码的时候邮箱token的验证
        :param token:
        :param new_password: 新密码
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        """
        用于生成邮箱更新的token，发送邮件
        :param new_email:
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        """
        用于验证邮箱更新的token
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        """
        判断用户是否拥有某项权限
        :param perm:
        :return:
        """
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """
        判断用户是否为超级管理员
        :return:
        """
        return self.can(Permission.ADMIN)

    def ping(self):
        """
        记录用于最近一次访问
        :return:
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def follow(self, user):
        """
        关注某个用户
        :param user:
        :return:
        """
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        """
        取消关注某个用户
        :param user:
        :return:
        """
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        """
        判断用户是否关注某个用户
        :param user:
        :return:
        """
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        """
        判断用户是否被某个用户关注
        :param user:
        :return:
        """
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        """
        用于查找当前用户id下follow的所有人的post发言记录，
        select Follow.follower_id, Follow.followed_id, Post.author_id, Post.body
            from Follow, Post
            where Follow.follower_id=self.id           # 获取全部的关注者id
                and Follow.followed_id=Post.author_id  # 获取这些关注者的post发言
        或者可以先从Follow中获取全部的关注者id，然后join到Post表中

        db.session.query(Post).select_from(Follow).\
            filter_by(follower_id=self.id).\
            join(Post, Follow.followed_id == Post.author_id)

        或者简化为返回值的形式
        Post.query.join(Follow, Follow.followed_id == Post.author_id). \  # 先把Post和Follow合并，得到一个大的表
            filter(Follow.follower_id == self.id)
            # 然后再找出当前用户id下follow的所有人的post发言记录
            # 这种方式效率可能低一些，不过如果数据库内部优化查询，问题不大，目前有待考究
        :return:
        """
        return Post.query.join(Follow, Follow.followed_id == Post.author_id) \
            .filter(Follow.follower_id == self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    # ---------------------  api接口相关功能，已经停止使用，因为不同版本api可能有不同需求  -----
    # ---------------------  因此所有的api功能均由api内部的service实现  ------------------------

    def generate_auth_token(self, expiration):
        """
        用于api接口，因为是无状态访问，因此每次用户访问需要携带token
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
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

    def to_json(self):
        """
        用于api接口，返回josn格式的用户数据，其中不返回邮箱
        由于to_json可能随着api版本不同而改变，因此该功能被写到了api的service中
        :return:
        """
        json_user = {
            'url': url_for('api/v1.0.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api/v1.0.get_user_posts', id=self.id),
            'followed_posts_url': url_for('api/v1.0.get_user_followed_posts',
                                          id=self.id),
            'post_count': self.posts.count()
        }
        return json_user

    # ---------------------  停止使用的功能如下 -------------------

    @staticmethod
    def add_self_follows():
        """
        在数据库没有出现follow之前已经建库情况下，补充自己关联自己，目前可以不用该函数
        :return:
        """
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def gravatar_hash(self):
        """
        用于生成avatar的hash值，由于gravatar网址国内无法访问，因此该功能被废除
        :return:
        """
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        """
        用于生成gravatar的网址，由于gravatar网址国内无法访问，因此该功能被废除
        :return:
        """
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
