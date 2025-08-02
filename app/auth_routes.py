import email
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User
from passlib.context import CryptContext
from .utils.security import pwd_context




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

        return jsonify({"msg": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return jsonify({"msg": "Invalid credentials"}), 401


        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    print("Incoming email:", data['email'])
    print("Incoming password:", data['password'])
    print("Stored hash:", user.password)

    result = pwd_context.verify(data['password'], user.password)
    print("Password verified:", result)
