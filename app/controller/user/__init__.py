from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

# 这一步的意义在于，加载views页面，否则views页面将不会被自动加载
from . import views
