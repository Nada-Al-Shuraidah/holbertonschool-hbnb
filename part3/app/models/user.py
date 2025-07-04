import re
from app import db, bcrypt
from .base_model import BaseModel
from sqlalchemy.orm import validates

_EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)
        else:
            raise ValueError("Password is required.")

    def hash_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    @validates('email')
    def validate_email(self, key, address):
        if not _EMAIL_RE.match(address):
            raise ValueError("Invalid email format.")
        return address

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
