from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "KasiLink API is running"}), 200
