from flask import Flask
from .extensions import db,ma



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    ma.init_app(app)

    from .routes import posts_bp
    app.register_blueprint(posts_bp)


    return app

    
