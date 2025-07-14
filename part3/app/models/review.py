# app/models/review.py

from app.extensions import db
from .base_model import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    rating   = db.Column(db.Integer, nullable=False)
    comment  = db.Column(db.Text, nullable=True)
    user_id  = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    reviewer = db.relationship("User", back_populates="reviews")
    place    = db.relationship("Place", back_populates="reviews")

    def __init__(self, comment, rating, place, user):
        if not isinstance(rating, int) or not (0 <= rating <= 5):
            raise ValueError("rating must be an integer between 0 and 5")
        super().__init__()
        self.comment = comment
        self.rating = rating
        self.place = place
        self.reviewer = user
