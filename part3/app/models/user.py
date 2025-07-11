# app/models/user.py

from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = 'users'

    # Track used emails for uniqueness
    _used_emails = set()

    # Columns
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(128), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=True)
    is_admin   = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email):
        # 1) First name length check
        if len(first_name) > 50:
            raise ValueError("first_name must be 50 characters or fewer")
        # 2) Unique email
        if email in User._used_emails:
            raise ValueError("email already used")
        super().__init__()  # sets id, created_at, updated_at
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        User._used_emails.add(email)

    # Relationships
    places = relationship(
        "Place",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review",
        back_populates="reviewer",
        cascade="all, delete-orphan"
    )
