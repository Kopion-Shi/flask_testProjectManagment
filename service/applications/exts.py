from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_security import Security

sqlAlchemy_db: SQLAlchemy = SQLAlchemy()

security: Security = Security()
jwt: JWTManager = JWTManager()
login_manager = LoginManager()
