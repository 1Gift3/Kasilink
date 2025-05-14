from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from .models import Post, User
from .extensions import db 


class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        include_fk = True  # Ensure foreign keys are included
    
    user_id = fields.Integer(dump_only=True) 
    user = fields.Nested('UserSchema', only=['username'])  # Include nested user data

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ("password",)  # Optional: hides password in response        

class SimplePostSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)


