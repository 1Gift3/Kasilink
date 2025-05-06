from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Post
from .extensions import ma

class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        sqla_session = ma.SQLAlchemy().session  # Optional; or skip if not used
