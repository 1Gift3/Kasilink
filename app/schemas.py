from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Post, User
from .extensions import db  # we only need db now
from datetime import datetime

class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        sqla_session = db.session

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ("password",)  # Optional: hides password in response        


