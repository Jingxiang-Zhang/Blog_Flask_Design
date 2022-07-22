from flask import Blueprint

test_web_safety_blueprint = Blueprint('test/web_safety', __name__)

from . import views
