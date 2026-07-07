from flask import Flask
from db import db
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app    )
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from app.models import (
    category_model,
    product_model,
    user_model
)

from app import router