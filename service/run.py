from flask import Flask, jsonify
from flask_cors import CORS
from applications.exts import db,jwt,login_manager,db_mg
from applications.controllers.product import app_product
from applications.controllers.user import app_user
from applications.controllers.dashboard import test_dashboard
from applications.controllers.applications import app_application
from applications.controllers.testmanager import test_manager
from config import config


app = Flask(__name__, static_folder="static")

app.config.from_object(config)
CORS(app, supports_credentials=True)
db.init_app(app=app)
jwt.init_app(app)
login_manager.init_app(app)
db_mg.init_app(app=app)
app.register_blueprint(app_user)
app.register_blueprint(app_product)
app.register_blueprint(test_dashboard)
app.register_blueprint(app_application)
app.register_blueprint(test_manager)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
