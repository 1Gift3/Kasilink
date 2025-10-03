from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import ServiceRequest, ServiceOffer

services_bp = Blueprint('services', __name__)


@services_bp.route('/requests', methods=['POST'])
@jwt_required()
def create_request():
    data = request.get_json() or {}
    required = ['title', 'description', 'category']
    for r in required:
        if r not in data:
            return jsonify({'error': f'{r} is required'}), 400

    try:
        latitude = float(data.get('latitude')) if data.get('latitude') is not None else None
        longitude = float(data.get('longitude')) if data.get('longitude') is not None else None
        radius_km = float(data.get('radius_km', 10.0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid latitude/longitude/radius_km'}), 400

    user_id = int(get_jwt_identity())

    sr = ServiceRequest(
        title=str(data.get('title')),
        description=str(data.get('description')),
        category=str(data.get('category')),
        budget=data.get('budget'),
        location=data.get('location'),
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        user_id=user_id
    )
    db.session.add(sr)
    db.session.commit()
    return jsonify({'message': 'ServiceRequest created', 'id': sr.id}), 201


@services_bp.route('/offers', methods=['POST'])
@jwt_required()
def create_offer():
    data = request.get_json() or {}
    required = ['title', 'description', 'category']
    for r in required:
        if r not in data:
            return jsonify({'error': f'{r} is required'}), 400

    try:
        latitude = float(data.get('latitude')) if data.get('latitude') is not None else None
        longitude = float(data.get('longitude')) if data.get('longitude') is not None else None
        radius_km = float(data.get('radius_km', 10.0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid latitude/longitude/radius_km'}), 400

    user_id = int(get_jwt_identity())

    so = ServiceOffer(
        title=str(data.get('title')),
        description=str(data.get('description')),
        category=str(data.get('category')),
        hourly_rate=data.get('hourly_rate'),
        location=data.get('location'),
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        user_id=user_id
    )
    db.session.add(so)
    db.session.commit()
    return jsonify({'message': 'ServiceOffer created', 'id': so.id}), 201


@services_bp.route('/matches/<int:request_id>', methods=['GET'])
def get_matches(request_id):
    sr = db.session.get(ServiceRequest, request_id)
    if not sr:
        return jsonify({'error': 'ServiceRequest not found'}), 404

    offers = sr.match(session=db.session)

    def _offer_to_dict(o):
        return {
            'id': o.id,
            'title': o.title,
            'description': o.description,
            'category': o.category,
            'hourly_rate': o.hourly_rate,
            'location': o.location,
            'latitude': o.latitude,
            'longitude': o.longitude,
            'radius_km': o.radius_km,
            'user_id': o.user_id
        }

    return jsonify([_offer_to_dict(o) for o in offers]), 200
