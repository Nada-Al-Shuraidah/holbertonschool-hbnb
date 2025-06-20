import re
from .base_model import BaseModel

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
    """
    _used_emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        # Name length validations
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or fewer.")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or fewer.")

        # Email validations
        # 1. Presence
        if not email:
            raise ValueError("Email is required.")
        # 2. Format
        if not _EMAIL_RE.match(email):
            raise ValueError("Invalid email format.")
        # 3. Uniqueness
        if email in User._used_emails:
            raise ValueError("Email must be unique.")
        User._used_emails.add(email)

        # Assign attributes
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.is_admin   = is_admin
