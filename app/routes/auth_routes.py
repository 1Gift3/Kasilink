import email
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models import db, User, Post
from ..schemas import PostSchema
from passlib.context import CryptContext
from ..utils.security import pwd_context


auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')



@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

          
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        return jsonify({"error": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id))
        print("Token identity type:", type(str(user.id)))
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "username": user.username,
        "email": user.email
    })

@auth_bp.route('/profile' , methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if 'username' in data:
        user.username = data['username']
    if 'email':
        user.email = email
        
    try:
        db.session.commit()
        return jsonify({"error": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500    
        

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'Both current and new passwords are required'}), 400

    if not pwd_context.verify(current_password, user.password_hash):
        return jsonify({'error': 'Current password is incorrect'}), 401

    user.set_password(new_password)
    try: 
        db.session.commit()
        return jsonify({'error': 'Password changed successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200


