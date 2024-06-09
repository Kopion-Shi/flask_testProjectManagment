from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from flask_mongoengine import MongoEngine
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
db: SQLAlchemy = SQLAlchemy()
db_mg: MongoEngine = MongoEngine()
jwt: JWTManager = JWTManager()


security = Security()
