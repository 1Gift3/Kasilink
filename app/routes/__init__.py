from flask import Flask
from app.extensions import db, migrate, jwt
from .auth_routes import auth_bp
from .posts_routes import posts_bp
from .main_routes import main_bp



def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')
    app.config["DEBUG"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(posts_bp, url_prefix='/posts')
    #app.register_blueprint(posts_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    
    return app
