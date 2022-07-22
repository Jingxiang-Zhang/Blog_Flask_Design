import flask_migrate
from app import create_app, db
from flask_script import Manager
from flask import redirect, url_for
# python manager.py sslrun
# python manager.py run
from flask_uploads import configure_uploads
from app.test import load_test_blueprint
from scripts.testing_route import get_route

from scripts.config import CheckPwd

with open("key.txt") as file:
    key = file.read().strip()
config_dict = CheckPwd.check_pwd_input_with_force("config.data",
                                                  group=("emile", "sql", "key", "sql_dev", "page", "img"))
app = create_app(config_dict)
flask_migrate.Migrate(app, db)
manager = Manager(app)


@manager.command
def db(option):
    """
    数据库迁移或初始化
    :param option: init, upgrade
    :return:
    """
    if option == "init":
        flask_migrate.init()
        flask_migrate.migrate()
        flask_migrate.upgrade()
        # 初始化角色列表
        from app.models.role import Role
        Role.insert_roles()
    elif option == "upgrade":
        flask_migrate.migrate()
        flask_migrate.upgrade()
        # 初始化角色列表
        from app.models.role import Role
        Role.insert_roles()
    elif option == "generate_fake":
        import scripts.fake as fake
        fake.fake_users(count=100, moderator_rate=0.2)
        fake.fake_posts(count_per_user=5, poisson=True)
        fake.fake_follows(follow_per_user=5, poisson=True)
        fake.fake_comments(comment_rate=0.4, comment_per_post=5, poisson=True)

        from scripts.fake.fake_profile import fake_profile
        fake_profile(r"D:\image_folder", r"img.jpg", max_img=100)  # you need to provide a folder full with image
        pass
    else:
        print("option can only be \"init\" or \"upgrade\"")


@manager.command
def sslrun():
    """
    from flask_sslify import SSLify
    SSLify(app)
    app.run(host="127.0.0.1", port=443, threaded=True, ssl_context="adhoc")
    """
    pass


@manager.command
def run():
    load_test_blueprint(app)  # 导入测试模块
    get_route(app=app, route_group=("/api/v1.0/",), show=True)  # 查看route_group的所有route
    app.run(host="127.0.0.1", port=80, threaded=True, debug=False)


manager.run()
