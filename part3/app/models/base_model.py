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
        # let SQLAlchemy set up the object
        super().__init__(*args, **kwargs)
        now = datetime.utcnow()
        # ensure each instance has its own UUID immediately
        if not getattr(self, "id", None):
            self.id = str(uuid.uuid4())
        # override any SQL-level defaults with real Python datetimes
        self.created_at = now
        self.updated_at = now

    def save(self):
        """Simulate saving by updating the timestamp only."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Apply a dict of changes, then bump updated_at."""
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
