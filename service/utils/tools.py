from functools import wraps
from flask import abort, request, redirect, url_for
def to_json(obj):
    dict = obj.__dict__
    if "_sa_instance_state" in dict:
        del dict["_sa_instance_state"]
        return dict
    

def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)  # 如果没有权限，则返回403禁止访问
            return f(*args, **kwargs)
        return wrapper
    return decorator