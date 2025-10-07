from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields
from app.models import Post, User, ServiceRequest, ServiceOffer
from app.extensions import db


class PostSchema(SQLAlchemyAutoSchema):
    category = fields.String(required=False)
    location = fields.String(required=False)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)

    class Meta:
        model = Post
        load_instance = True
        include_fk = True
        sqla_session = db.session

    user = fields.Nested('UserSchema', only=['username'])
    user_id = fields.Integer(dump_only=True)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session


class SimplePostSchema(Schema):
    title = fields.Str(required=True)
    content = fields.Str(required=True)


class ServiceRequestSchema(SQLAlchemyAutoSchema):
    title = fields.String(required=True)
    description = fields.String(required=False, allow_none=True)
    category = fields.String(required=True)
    budget = fields.Float(required=False, allow_none=True)
    location = fields.String(required=False, allow_none=True)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    radius_km = fields.Float(required=False, allow_none=True)
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = ServiceRequest
        load_instance = True
        include_fk = True
        sqla_session = db.session


class ServiceOfferSchema(SQLAlchemyAutoSchema):
    title = fields.String(required=True)
    description = fields.String(required=False, allow_none=True)
    category = fields.String(required=True)
    hourly_rate = fields.Float(required=False, allow_none=True)
    location = fields.String(required=False, allow_none=True)
    latitude = fields.Float(required=False, allow_none=True)
    longitude = fields.Float(required=False, allow_none=True)
    radius_km = fields.Float(required=False, allow_none=True)
    user_id = fields.Integer(dump_only=True)

    class Meta:
        model = ServiceOffer
        load_instance = True
        include_fk = True
        sqla_session = db.session