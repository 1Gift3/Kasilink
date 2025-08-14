from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Post
from app.extensions import db

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Missing required fields"}), 400
    if not isinstance(data['title'], str) or not isinstance(data['content'], str):
        return jsonify({"error": "Invalid data type"}), 400

    user_id = get_jwt_identity()
    new_post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully", "id": new_post.id}), 201


@posts_bp.route('/posts', methods=['GET'], strict_slashes=False)
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": p.id, "title": p.title, "content": p.content} for p in posts]), 200


@posts_bp.route('/posts/<int:post_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()

    return jsonify({"message": "Post updated successfully"}), 200


@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"}), 200
