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
        # assign a new UUID immediately if none provided
        if 'id' not in kwargs or kwargs.get('id') is None:
            kwargs['id'] = str(uuid.uuid4())
        super().__init__(*args, **kwargs)

    def save(self):
        """Just update the `updated_at` timestamp—no DB calls here."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update fields from dict and bump timestamp."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Dump all column values to a dict."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        """Print as: [ClassName] (id) { … }"""
        cls = self.__class__.__name__
        return f"[{cls}] ({self.id}) {self.to_dict()}"
