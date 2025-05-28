from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from utils.db_utils import create_db_pool
from routes.auth import register_auth_routes
from routes.model import register_model_routes
from routes.tests import register_test_routes
from utils.model_utils import MistralClient
from config import MODEL_CONFIG, APP_CONFIG
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

db_pool = create_db_pool()
model = MistralClient(MODEL_CONFIG["BASE_URL"], MODEL_CONFIG["API_KEY"], MODEL_CONFIG["MODEL_NAME"])

# Routes
register_auth_routes(app, db_pool)
register_model_routes(app, model, db_pool)
register_test_routes(app, db_pool)

if __name__ == "__main__":
    port = APP_CONFIG["PORT"]
    app.run(debug=True, host=APP_CONFIG["HOST"], port=port)
