from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Check for existing user
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    # Create user and assign password via the property setter to ensure hashing
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    # assign password using the property setter
    new_user.password = data['password']
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    # allow login by username or email
    username = data.get('username')
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Generate JWT token (if using Flask-JWT)
    # JWT subject is expected to be a string by newer pyjwt checks; store id as string
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200


@auth_bp.route('/protected', methods=['GET'], strict_slashes=False)
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Hello user {current_user_id}, this is a protected route"}), 200
