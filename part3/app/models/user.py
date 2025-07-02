import re
from .base_model import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

_EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

class User(BaseModel):
    _used_emails = set()

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()

        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or fewer.")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or fewer.")
        if not email:
            raise ValueError("Email is required.")
        if not _EMAIL_RE.match(email):
            raise ValueError("Invalid email format.")
        if email in User._used_emails:
            raise ValueError("Email must be unique.")
        User._used_emails.add(email)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password_hash = None
        self.password = None  # optional field for clarity

        if password:
            self.hash_password(password)

    def hash_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = super().to_dict()
        data.pop('password_hash', None)
        return data
