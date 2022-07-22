from functools import wraps
from flask import abort
from flask_login import current_user
from .models.role import Permission

def permission_required(permission):
    """
    用于检验用户是否具有某种权限，如果否，则直接发生403错误
    eg:
    @permission_required(A)
    def test(n):
        return n
    A权限进入permission_required，直接返回decorator(f)函数
    decorator(f) 继续接受test函数，f=test
    继续执行 decorated_function, 其接受的参数被test的参数n赋值，
    由此，permission=A，f=test，*args**kwargs=n
    @wrap的作用是，不改变被permission_required修饰者的__name__函数名，和__doc__，注释说明
    :param permission: 用户是否具有的权限
    :return:
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
