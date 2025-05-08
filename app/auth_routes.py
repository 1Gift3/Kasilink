from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import db, User



auth_bp = Blueprint('auth_bp', __name__)



@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Missing username or password"}), 400

        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({"msg": "User already exists"}), 409

        hashed_pw = generate_password_hash(data['password'])
        new_user = User(username=data['username'], password=hashed_pw)
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data.get('username') or not data.get('password'):
            return jsonify({"msg": "Missing username or password"}), 400

        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"msg": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500