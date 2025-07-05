from .base_model import BaseModel
from app.extensions import db
from sqlalchemy.orm import relationship

# Association table for many-to-many: Place <-> Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign Key to User
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # One-to-Many: Place -> Review
    reviews = relationship('Review', backref='place', lazy=True)

    # Many-to-Many: Place <-> Amenity
    amenities = relationship('Amenity', secondary=place_amenity, lazy='subquery',
                             backref=db.backref('places', lazy=True))
