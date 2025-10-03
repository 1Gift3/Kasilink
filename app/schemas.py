from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from app.models import Post, User
from .extensions import db 


class PostSchema(SQLAlchemyAutoSchema):
    category = fields.String(required=False)   # add this line
    location = fields.String(required=False)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    
    class Meta:
        model = Post
        load_instance = True
        include_fk = True
        sqla_session = db.session

    user = fields.Nested('UserSchema', only=['username'])  # shows username from related user
    user_id = fields.Integer(dump_only=True)  # don't expect user_id in incoming JSON

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

class SimplePostSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)



