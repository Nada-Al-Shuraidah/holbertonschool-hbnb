from .base_model import BaseModel
from app.extensions import db

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default='')
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
