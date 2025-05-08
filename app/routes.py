from flask import Blueprint, request, jsonify
from .models import Post, db
from .schemas import PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity


posts_bp = Blueprint('posts_bp', __name__, url_prefix='/posts')
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

@posts_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    return jsonify(msg=f"Hello, user {user_id}")

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    all_posts = Post.query.all()
    return jsonify(posts_schema.dump(all_posts)), 200


@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    errors = post_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Manually assign user_id to the post
    new_post = Post(title=data['title'], content=data['content'], user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return jsonify(post_schema.dump(new_post)), 201




