from flask import Flask
from flask_cors import CORS

from api.pruduct import app_product
from api.user import app_user
from api.applications import app_application
from api.testmanager import test_manager

app = Flask(__name__, static_folder="static")
CORS(app, supports_credentials=True)
app.register_blueprint(app_user)
app.register_blueprint(app_product)
app.register_blueprint(app_application)
app.register_blueprint(test_manager)

if __name__ == "__main__":
    app.run(debug=True)
