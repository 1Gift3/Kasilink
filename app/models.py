from datetime import datetime
from app import db
from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean, DateTime


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', String(128))  # Note the underscore
    
    @property
    def password(self):
        raise AttributeError("Password not readable")
    
    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self._password, password)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50))  
    location = db.Column(db.String(100))
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False) 
    
    user = db.relationship('User', backref=db.backref('posts' , lazy=True))
    


class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    budget = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    radius_km = db.Column(db.Float, default=10.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('service_requests', lazy=True))

    def match(self, session=None):
        """Return ServiceOffer objects in same category and within radius_km.

        This is a simple, DB-agnostic implementation that loads candidate offers
        with coordinates and filters in Python using the Haversine formula.
        For production, replace with a spatial index (PostGIS) or bounding-box filter.
        """
        from math import radians, sin, cos, atan2, sqrt

        def haversine_km(lat1, lon1, lat2, lon2):
            R = 6371.0
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c

        if self.latitude is None or self.longitude is None:
            return []

        # Use provided session or the global db.session
        session = session or db.session

        candidates = session.query(ServiceOffer).filter(
            ServiceOffer.category == self.category,
            ServiceOffer.latitude.isnot(None),
            ServiceOffer.longitude.isnot(None)
        ).all()

        results = []
        for offer in candidates:
            dist = haversine_km(self.latitude, self.longitude, offer.latitude, offer.longitude)
            if dist <= (self.radius_km or 0):
                results.append((offer, dist))

        # sort by distance
        results.sort(key=lambda x: x[1])
        return [o for o, d in results]


class ServiceOffer(db.Model):
    __tablename__ = 'service_offers'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    radius_km = db.Column(db.Float, default=10.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('service_offers', lazy=True))



