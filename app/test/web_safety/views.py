from . import test_web_safety_blueprint
from flask import request, render_template


@test_web_safety_blueprint.route('/')
def index():
    return render_template("test/web_safety/index.html")


@test_web_safety_blueprint.route('/http_headers')
def http_headers():
    http_headers = str(request.headers).split("\n")
    ip = request.remote_addr
    user_hop = request.access_route
    return render_template('test/web_safety/http_headers.html', http_headers=http_headers,
                           ip=ip, user_hop=user_hop)


@test_web_safety_blueprint.route('/referer')
def referer():
    referer = request.referrer
    success = (referer == "www.baidu.com")
    return render_template('test/web_safety/referer.html', referer=referer, success=success)
