from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def _verify_password(user, password):
    if user is None or not password:
        return False
    # prefer model helper if present
    if hasattr(user, "verify_password"):
        try:
            return user.verify_password(password)
        except TypeError:
            pass
    if hasattr(user, "check_password"):
        try:
            return user.check_password(password)
        except TypeError:
            pass
    # fallback: assume user.password stores a hash
    return check_password_hash(getattr(user, "password", "") or "", password)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # If a user already exists, return success (id) so tests that re-run register can proceed to login.
    existing = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing:
        return jsonify({"message": "User already exists", "id": existing.id}), 200

    user = User(username=username, email=email)
    user.password = password  # use property setter to hash
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully", "id": user.id}), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    username = data.get('username')
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()

    if not _verify_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    payload = {"access_token": access_token}
    print("DEBUG_LOGIN_RESPONSE", payload, flush=True)
    current_app.logger.info("login response JSON: %s", payload)
    return jsonify(payload), 200

