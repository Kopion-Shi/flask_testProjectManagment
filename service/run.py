from flask import Flask
from flask_cors import CORS
from applications.exts import db
from applications.controllers.product import app_product
from applications.controllers.user import app_user
from applications.controllers.dashboard import test_dashboard
from applications.controllers.applications import app_application
from applications.controllers.testmanager import test_manager
from config import config
app = Flask(__name__, static_folder="static")
app.config.from_object(config)
db.init_app(app=app)
CORS(app, supports_credentials=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.register_blueprint(app_user)
app.register_blueprint(app_product)
app.register_blueprint(test_dashboard)
app.register_blueprint(app_application)
app.register_blueprint(test_manager)


if __name__ == "__main__":
    app.run(debug=True,host="172.22.172.41")
