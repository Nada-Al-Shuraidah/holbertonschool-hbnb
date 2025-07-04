import uuid
from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True  # يمنع SQLAlchemy من إنشاء جدول لهذا الكلاس

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
