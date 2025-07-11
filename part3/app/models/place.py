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

    # 1) Change backref → back_populates
    owner = relationship(
        'User',
        back_populates='places'
    )
    # 2) Change backref → back_populates
    reviews = relationship(
        'Review',
        back_populates='place',
        cascade='all, delete-orphan'
    )
    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        backref=db.backref('places', lazy=True),
        lazy='subquery'
    )
