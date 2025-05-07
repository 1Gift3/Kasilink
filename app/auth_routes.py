from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .models import db, User

auth_bp = Blueprint('auth_bp', __name__)  # Make sure blueprint name is not a URL

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
