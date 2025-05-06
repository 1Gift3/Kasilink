from flask import Flask
from .routes import posts_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    
    app.register_blueprint(posts_bp)


    return app

    
