import re
from .base_model import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Simple email regex: something@something.something
_EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

class User(BaseModel):
    """
    A person using the Hbnb platform.

    Attributes:
      first_name (str): up to 50 chars.
      last_name  (str): up to 50 chars.
      email      (str): required, valid format, unique.
      is_admin   (bool): defaults to False.
      password_hash (str): hashed password, not returned in responses.
    """
    _used_emails = set()

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()

        # Name validations
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or fewer.")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or fewer.")

        # Email validations
        if not email:
            raise ValueError("Email is required.")
        if not _EMAIL_RE.match(email):
            raise ValueError("Invalid email format.")
        if email in User._used_emails:
            raise ValueError("Email must be unique.")
        User._used_emails.add(email)

        # Assign attributes
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        # Set password if provided
        if password:
            self.set_password(password)
        else:
            self.password_hash = None

    def set_password(self, password):
        """Hashes the password and stores it."""
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if a plain password matches the hashed one."""
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Returns a dictionary representation without sensitive fields."""
        data = super().to_dict()
        data.pop('password_hash', None)  # Don't expose password hash
        return data
