from flask import Blueprint, render_template
from .web_safety import test_web_safety_blueprint

test_blueprint = Blueprint('test', __name__)


def load_test_blueprint(app):
    app.register_blueprint(test_blueprint, url_prefix='/test')
    app.register_blueprint(test_web_safety_blueprint, url_prefix='/test/web_safety')


@test_blueprint.route("/")
def index():
    return render_template("test/index.html")
