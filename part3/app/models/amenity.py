from .base_model import BaseModel
from app.extensions import db
from .place_amenity import place_amenity

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    # Many-to-Many: Places that include this amenity
    places = db.relationship(
        "Place",
        secondary=place_amenity,
        backref=db.backref("amenities", lazy="subquery"),
        lazy="subquery"
    )
