from flask_login import UserMixin  # 引入用户基类
from service.applications.exts import db_mg
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required

db = db_mg


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
