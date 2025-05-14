from flask import Blueprint, request, jsonify, current_app
from .models import Post, db
from .schemas import PostSchema, SimplePostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy


posts_bp = Blueprint('posts_bp', __name__, url_prefix='/posts')
post_schema = PostSchema(session=db.session)
#posts_schema = PostSchema(many=True)

@posts_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    return jsonify(msg=f"Hello, user {user_id}"), 200
    #return jsonify(msg=f"Hello, user {user_id}, you're successfully authenticated!"), 200

#@posts_bp.route('/posts', methods=['GET'])
#def get_posts():
#    all_posts = Post.query.all()
#    return jsonify(posts_schema.dump(all_posts)), 200

@posts_bp.route('/test', methods=['POST'])
def test_post():
    return jsonify({"msg": "Test route is working!"}), 200



@posts_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    post_schema = PostSchema()
    try:
        # Load the post data from the request
        post_data = post_schema.load(request.get_json())

        # Get the user_id from the request data
        user_id = post_data.get('user_id')
        
        # Check if the user exists in the database
        user = user.query.get(user_id)  # Fetch the user by user_id
        
        if not user:
            return {"message": f"User with ID {user_id} not found."}, 404  # Return 404 if user does not exist
        
        # Create a new post instance if the user exists
        post = Post(**post_data)
        
        # Create a new post instance
        post = Post(**post_data)

        db.session.add(post)
        db.session.commit()

        return jsonify(post_schema.dump(post)), 201
    except Exception as e:
        # Log or print the exception to get more insight into what's failing
        print(f"Error: {e}")
        return {"message": "Error creating post"}, 500




