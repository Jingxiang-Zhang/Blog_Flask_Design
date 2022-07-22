from flask import Blueprint

api_blueprint_v1_0 = Blueprint('api/v1.0', __name__)

# 这一步的意义在于，加载全部的route的py文件，否则这些py文件将不会被自动加载
from . import authorization
from . import decorators
from .routes import users
from .routes import comments
from .routes import posts

