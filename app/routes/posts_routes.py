from flask import Blueprint, request, jsonify
from math import radians, cos, sin, asin, sqrt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import Post
from app.extensions import db

from app.models import Post
from app.schemas import PostSchema

posts_bp = Blueprint("posts", __name__, url_prefix="/posts")

def _haversine_km(lat1, lon1, lat2, lon2):
    if None in (lat1, lon1, lat2, lon2):
        return None
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return R * c


@posts_bp.route("/", methods=["GET"])
def list_posts():
    """
    GET /posts
    Query params:
      - user_id (int)
      - lat, lon, radius_km (floats) -> spatial filter (returns distance_km)
      - page (int, default=1) & limit (int, default=20) -> offset/limit pagination
      - Or cursor-based: ?after_id=<last_seen_id>&limit=20 (optional)
    """
    q = Post.query
    user_id = request.args.get("user_id", type=int)
    if user_id:
        q = q.filter_by(user_id=user_id)

    # pagination params
    page = max(1, request.args.get("page", type=int, default=1))
    limit = request.args.get("limit", type=int, default=20)
    limit = max(1, min(limit, 100))  # cap limit to 100
    offset = (page - 1) * limit

    # optional cursor pagination
    after_id = request.args.get("after_id", type=int)

    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius_km = request.args.get("radius_km", type=float)

    if lat is not None and lon is not None and radius_km is not None:
        # bounding-box prefilter
        lat_delta = radius_km / 111.32
        lon_delta = radius_km / (111.32 * max(0.000001, abs(cos(radians(lat)))))

        min_lat = lat - lat_delta
        max_lat = lat + lat_delta
        min_lon = lon - lon_delta
        max_lon = lon + lon_delta

        q = q.filter(
            Post.latitude.isnot(None),
            Post.longitude.isnot(None),
            Post.latitude.between(min_lat, max_lat),
            Post.longitude.between(min_lon, max_lon),
        )

        # apply cursor if provided (helps paginate deterministically by id)
        if after_id:
            q = q.filter(Post.id > after_id)

        candidates = q.all()  # small result set after bbox; if large, consider SQL limit
        nearby = []
        for p in candidates:
            d = _haversine_km(lat, lon, p.latitude, p.longitude)
            if d is not None and d <= radius_km:
                nearby.append((d, p))

        nearby.sort(key=lambda x: x[0])
        posts_slice = nearby[offset: offset + limit]
        posts = []
        for d, p in posts_slice:
            item = PostSchema().dump(p)
            item["distance_km"] = round(d, 3)
            posts.append(item)

        # metadata for client pagination
        total_matches = len(nearby)
        return jsonify({
            "page": page,
            "limit": limit,
            "total": total_matches,
            "items": posts
        }), 200

    # Non-spatial path: use offset/limit at SQL level for performance
    if after_id:
        q = q.filter(Post.id > after_id).order_by(Post.id.asc())
        posts_objs = q.limit(limit).all()
        # cursor-style response (next after_id can be last item's id)
        next_after = posts_objs[-1].id if posts_objs else None
        items = PostSchema(many=True).dump(posts_objs)
        return jsonify({"after_id": next_after, "limit": limit, "items": items}), 200

    posts_objs = q.order_by(Post.created_at.desc()).offset(offset).limit(limit).all()
    items = PostSchema(many=True).dump(posts_objs)
    return jsonify({
        "page": page,
        "limit": limit,
        "items": items
    }), 200


@posts_bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    p = Post.query.get_or_404(post_id)
    schema = PostSchema()
    return jsonify(schema.dump(p)), 200

@posts_bp.route("/posts", methods=['POST'], strict_slashes=False)
@posts_bp.route("/", methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Coerce title/content to strings to be permissive (tests expect non-string inputs to be accepted)
    try:
        title = str(data.get('title'))
        content = str(data.get('content'))
    except Exception:
        return jsonify({"error": "Invalid title/content"}), 400

    user_id = int(get_jwt_identity())
    # accept optional location and coordinates
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    location = data.get('location')

    # basic validation for coordinates if provided
    try:
        latitude = float(latitude) if latitude is not None else None
        longitude = float(longitude) if longitude is not None else None
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid latitude/longitude"}), 400

    new_post = Post(title=title, content=content, user_id=user_id,
                    location=location, latitude=latitude, longitude=longitude)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully", "id": new_post.id}), 201


@posts_bp.route("/", methods=['GET'], strict_slashes=False)
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": p.id, "title": p.title, "content": p.content, "location": p.location,
                     "latitude": p.latitude, "longitude": p.longitude} for p in posts]), 200


def _haversine_km(lat1, lon1, lat2, lon2):
    """Return distance between two lat/lon pairs in kilometers."""
    from math import radians, sin, cos, atan2, sqrt

    R = 6371.0  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


@posts_bp.route("/nearby", methods=['GET'], strict_slashes=False)
def nearby_posts():
    """Query params: lat, lon, radius_km (default 5km). Returns posts within radius that have coordinates."""
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
    except (TypeError, ValueError):
        return jsonify({"error": "lat and lon query parameters are required and must be numbers"}), 400

    try:
        radius_km = float(request.args.get('radius_km', 5.0))
    except ValueError:
        return jsonify({"error": "radius_km must be a number"}), 400

    posts = Post.query.filter(Post.latitude.isnot(None), Post.longitude.isnot(None)).all()

    results = []
    for p in posts:
        # safety: skip if coordinates missing
        if p.latitude is None or p.longitude is None:
            continue
        dist = _haversine_km(lat, lon, p.latitude, p.longitude)
        if dist <= radius_km:
            results.append({"id": p.id, "title": p.title, "content": p.content,
                            "location": p.location, "latitude": p.latitude,
                            "longitude": p.longitude, "distance_km": round(dist, 3)})

    # sort by distance
    results.sort(key=lambda x: x['distance_km'])
    return jsonify(results), 200


@posts_bp.route('/protected', methods=['GET'], strict_slashes=False)
@jwt_required()
def protected_posts():
    # simple protected endpoint used by tests
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello user {current_user}, this is a protected route"}), 200


@posts_bp.route("<int:post_id>", methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()

    return jsonify({"message": "Post updated successfully"}), 200


@posts_bp.route("<int:post_id>", methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted successfully"}), 200
