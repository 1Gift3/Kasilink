import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt_identity


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

logger = logging.getLogger("kasilink")
logger.setLevel(logging.DEBUG)