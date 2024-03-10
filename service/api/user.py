import json
from flask import Blueprint
from flask import request


app_user=Blueprint("app_user",__name__)


@app_user.route("/api/user/login", methods=["POST"])
def login():
    data = request.get_data()
    js_data = json.loads(data)

    if "username" in js_data and js_data["username"] == "admin":
        result = {"code": 20000, "data": {"token": "admin-token"}}

    else:
        result = {"code": 60204, "message": "账号密码错误，请检查"}

    return result


@app_user.route("/api/user/info", methods=["GET"])
def info():
    # 获取GET中请求token参数值
    token = request.args.get("token")
    if token == "admin-token":

        # basedir一般是在配置文件中
        result_success = {
            "code": 20000,
            "data": {
                "roles": ["admin"],
                "introduction": "I am a super administrator",
                "avatar": request.host_url + "static/avatar/1.gif",
                "name": "Super Admin",
            },
        }
        return result_success
    else:
        result_error = {"code": 60204, "message": "用户信息获取错误"}
        return result_error
