from flask import Flask
from .extensions import db, migrate, jwt
from .routes.auth_routes import auth_bp
from .routes.posts_routes import posts_bp
from .routes.main_routes import main_bp




def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    if test_config:
        app.config.update(test_config)

    app.config["DEBUG"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    return app
