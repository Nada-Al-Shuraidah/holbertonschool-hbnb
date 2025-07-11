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

    def save(self):
        """Add the object to the session and commit."""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update fields from dict and save changes."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return a dict of all column names/values."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __str__(self):
        """String format: [<ClassName>] (<id>) <dict of attrs>."""
        cls = self.__class__.__name__
        return f"[{cls}] ({self.id}) {self.to_dict()}"
