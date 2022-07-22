from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
import os

bootstrap = Bootstrap()  # 用于bootstrap美化界面
mail = Mail()  # 用于发送邮件
moment = Moment()  # 用于分时区显示时间
db = SQLAlchemy()  # 用于数据库查询
pagedown = PageDown()  # 用于页面显示

login_manager = LoginManager()  # 用于用户登录控制
login_manager.login_view = 'auth.login'  # 记录用户初始化界面
base_dir = os.path.abspath(os.path.dirname(__file__))

# 导入模型，在初始化db对象后才能导入
from .models import *
from app.controller import *


def create_app(config_dict):


    templates_dir = os.path.join(base_dir, 'webapp/templates')
    static_dir = os.path.join(base_dir, 'webapp/static')
    app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)

    # 初始化全部的flask库
    app.config.from_mapping(config_dict)  # 加载配置参数
    app.config["MAIL_USE_SSL"]=True

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # 引入蓝图
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint_v1_0, url_prefix='/api/v1.0')
    app.register_blueprint(error_blueprint, url_prefix='/error')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    return app
