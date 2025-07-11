# app/models/place.py

from app.extensions import db
from .base_model import BaseModel
from .place_amenity import place_amenity
from .user import User
from sqlalchemy.orm import relationship

class Place(BaseModel):
    __tablename__ = 'places'

    title       = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    price       = db.Column(db.Float, nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    longitude   = db.Column(db.Float, nullable=False)
    user_id     = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # **This exact signature** so SQLAlchemy uses it:
    def __init__(self, title, description, price, latitude, longitude, owner):
        if not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        # **Call the BaseModel constructor with no extra args**
        super().__init__()
        self.title       = title
        self.description = description
        self.price       = price
        self.latitude    = latitude
        self.longitude   = longitude
        self.owner       = owner

    owner     = relationship("User", back_populates="places")
    reviews   = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    def add_amenity(self, amenity):
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
