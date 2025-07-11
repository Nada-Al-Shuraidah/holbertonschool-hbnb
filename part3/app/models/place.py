# app/models/place.py

from .base_model import BaseModel
from .place_amenity import place_amenity
from app.extensions import db
from sqlalchemy.orm import relationship

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    price       = db.Column(db.Float, nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    longitude   = db.Column(db.Float, nullable=False)
    user_id     = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description, price, latitude, longitude, owner):
        # No extra validation specified by tests
        super().__init__()
        self.title       = title
        self.description = description
        self.price       = price
        self.latitude    = latitude
        self.longitude   = longitude
        # Set relationship; SQLAlchemy will populate user_id
        self.owner = owner

    # Relationships
    owner     = relationship("User", back_populates="places")
    reviews   = relationship(
        "Review",
        back_populates="place",
        cascade="all, delete-orphan"
    )
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places"
    )
