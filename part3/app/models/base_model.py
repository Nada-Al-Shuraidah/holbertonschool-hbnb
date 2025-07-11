# app/models/base_model.py

import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __init__(self, *args, **kwargs):
        # Prepare Python-side defaults before SQLAlchemy magic
        now = datetime.utcnow()
        # Extract any passed-in values
        id_val = kwargs.pop('id', None)
        created_val = kwargs.pop('created_at', None)
        updated_val = kwargs.pop('updated_at', None)
        # Let SQLAlchemy set up the mapped attributes
        super().__init__(*args, **kwargs)
        # Now override with real Python values
        self.id = id_val or str(uuid.uuid4())
        self.created_at = created_val or now
        self.updated_at = updated_val or now

    def save(self):
        """Simulate saving by bumping only the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update attributes and bump updated_at."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return a dict of all column names and their values."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        """String representation: [ClassName] (id) { ... }."""
        cls = self.__class__.__name__
        return f"[{cls}] ({self.id}) {self.to_dict()}"
