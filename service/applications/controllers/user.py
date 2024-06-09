import json
from flask import Blueprint
from flask import request
from flask_security import LoginForm

app_user=Blueprint("app_user",__name__,url_prefix='/api/user/')

@app_user.route("login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app_user.route("info", methods=["GET"])
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
