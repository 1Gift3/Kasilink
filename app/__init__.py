from flask import Flask, app, jsonify
from flask_migrate import Migrate
from .extensions import db, jwt
from .routes.auth_routes import auth_bp
from .routes.posts_routes import posts_bp
from .routes.services_routes import services_bp
from app.routes import auth_bp, posts_bp, main_bp
from flask_jwt_extended import JWTManager


migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)
    
    if config_class is None:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(config_class)
        print("🔍 Running with config:", config_class.__name__)
        print("🔍 SQLALCHEMY_DATABASE_URI =", app.config.get("SQLALCHEMY_DATABASE_URI"))

    # Ensure JWT has a secret key configured (fallback to SECRET_KEY)
    if not app.config.get('JWT_SECRET_KEY'):
        app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY')

    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
     
    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"msg": "Invalid token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({"msg": "Missing token"}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token expired"}), 401
  

    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(main_bp)

    return app
