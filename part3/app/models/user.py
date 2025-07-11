from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = 'users'

    # --- 1) Track used emails for uniqueness ---------------------
    _used_emails = set()

    # --- 2) Columns ------------------------------------------------
    first_name = db.Column(db.String(128), nullable=False)
    last_name  = db.Column(db.String(128), nullable=False)
    email      = db.Column(db.String(128), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=True)
    is_admin   = db.Column(db.Boolean, default=False, nullable=False)

    # --- 3) Simplified constructor -------------------------------
    def __init__(self, first_name, last_name, email):
        # Enforce unique email at model-level
        if email in User._used_emails:
            raise ValueError("email already used")
        # BaseModel __init__ sets up id, created_at, updated_at
        super().__init__()
        # Assign business fields
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        # Mark this email as used
        User._used_emails.add(email)

    # --- 4) Relationships (matching back_populates on the other side)
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
