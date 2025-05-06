from flask import Blueprint, request, jsonify
from .models import Post, db
from .schemas import PostSchema

posts_bp = Blueprint('/posts', __name__)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@posts_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    errors = post_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_post = Post(**data)
    db.session.add(new_post)
    db.session.commit()

    return post_schema.jsonify(new_post), 201


@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    return posts_schema.jsonify(all_posts), 200