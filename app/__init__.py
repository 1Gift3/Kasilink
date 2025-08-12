from flask import Flask
from flask_migrate import Migrate
from .extensions import db, jwt
from .routes.auth_routes import auth_bp
from .routes.posts_routes import posts_bp
from .routes.main_routes import main_bp
from config import Config  # Import your config

migrate = Migrate()  # Ensure migrate is defined here

def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class is None:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app