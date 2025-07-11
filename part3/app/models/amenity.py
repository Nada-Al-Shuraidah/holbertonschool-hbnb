# app/models/amenity.py

from app.extensions import db
from .base_model import BaseModel
from .place_amenity import place_amenity
from sqlalchemy.orm import relationship

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        self.name = name

    # Many-to-many with explicit back_populates
    places = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities"
    )
