from flask import Blueprint, request, jsonify, current_app, abort
from ..models import User, Post, db
from ..schemas import PostSchema, SimplePostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import logger
from marshmallow import ValidationError



posts_bp = Blueprint('posts_bp', __name__, url_prefix='/posts')
post_schema = PostSchema(session=db.session)
#posts_schema = PostSchema(many=True)

@posts_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="User not found"), 404
    

    return jsonify({
        "msg": "Access Granted",
         "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
         } 
     }), 200
    #return jsonify(msg=f"Hello, user {user_id}, you're successfully authenticated!"), 200

#@posts_bp.route('/posts', methods=['GET'])
#def get_posts():
#    all_posts = Post.query.all()
#    return jsonify(posts_schema.dump(all_posts)), 200

@posts_bp.route('/test', methods=['POST'])
def test_post():
    return jsonify({"msg": "Test route is working!"}), 200



@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    try:
        user_id = get_jwt_identity()
        post_data = request.get_json()

        # Validate incoming data (without user_id)
        post = post_schema.load(post_data)

        # Set the user_id securely from JWT
        post.user_id = user_id

        db.session.add(post)
        db.session.commit()

        return jsonify(post_schema.dump(post)), 201

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 400

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating post: {e}")
        return jsonify({"message": "Error creating post"}), 500

        
    
@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.filter(Post.deleted == False).all() 
    posts_schema = PostSchema(many=True)
    return jsonify(posts_schema.dump(posts)), 200


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.filter_by(id=post_id, deleted=False).first_or_404()
    post_schema = PostSchema()
    return jsonify(post_schema.dump(post)), 200


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    try:
        user_id = int(get_jwt_identity())  # Force it to int
        post = Post.query.get_or_404(post_id)

        print(f"JWT user_id: {user_id} ({type(user_id)})")
        print(f"Post user_id: {post.user_id} ({type(post.user_id)})")

        if post.user_id != user_id:
            print("🚫 Authorization failed")
            return jsonify({"msg": "Unauthorized"}), 403

        post_schema = PostSchema(partial=True)
        data = request.get_json()
        post = post_schema.load(data, instance=post, partial=True)

        db.session.commit()
        return jsonify(post_schema.dump(post)), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating post: {e}")
        return jsonify({"msg": "Error updating post"}), 500



@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())
    post = Post.query.get_or_404(post_id)

    if post.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    try:
        post.deleted = True  # Soft delete
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "Post deleted"}), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting post: {e}")
        return jsonify({"msg": "Error deleting post"}), 500