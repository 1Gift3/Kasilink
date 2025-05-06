from flask import Blueprint, request, jsonify
from .models import posts

posts_bp = Blueprint('/posts', __name__)

@posts_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    required = {'title', 'content', 'category', 'location'}
    if not data or not required.issubset(data):
        return jsonify({'error': 'Missing required fields'}), 400

    posts.append(data)
    return jsonify({'message': 'Post created', 'post': data}), 201

    

@posts_bp.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts), 200

