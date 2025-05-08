from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt_identity

jwt = JWTManager()

db = SQLAlchemy()
migrate = Migrate()
