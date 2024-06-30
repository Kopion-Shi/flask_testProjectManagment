from flask import Blueprint, jsonify
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_login import login_required, login_user, logout_user, current_user
from applications.exts import sqlAlchemy_db as db
from applications.exts import login_manager
from service.applications.models.user import User

app_user = Blueprint("app_user", __name__, url_prefix='/api/user/')


@login_manager.user_loader
def user_loader(userid):
    # 这里应该是从数据库或其他地方根据 user_id 加载用户的代码
    return User.query.get(int(userid))


@login_manager.request_loader
@jwt_required()
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    userid = get_jwt_identity()
    user = User.query.get(int(userid))
    if api_key:
        if user:
            return user
        else:
            print("is exception !!!! error_msg")
            return None


@app_user.route("login", methods=["POST"])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.session.query(User).filter_by(username=username).first()
    if user and user.password_hash == password:
        login_user(user, remember=True)
        access_token = create_access_token(user.id)
        return jsonify({"code": 20000, "data": {"token": access_token}})
    else:
        return jsonify({"code": 60204, "message": "账号密码错误，请检查"})


@app_user.route("/info", methods=["POST", "GET"])
@login_required
def info():
    result_success = {
        "code": 20000,
        "data": {
            "roles": ["admin"],
            "introduction": "I am a super administrator",
            "avatar": request.host_url + "static/avatar/1.gif",
            "name": "Super Admin",
        },
    }
    return jsonify(result_success)


@app_user.route('/logout',methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"code": 20000, "message": "Logout successful"})
