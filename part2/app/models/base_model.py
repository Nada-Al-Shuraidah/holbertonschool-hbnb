import uuid
from datetime import datetime

class BaseModel:
    """Core functionality: unique ID plus created/updated timestamps."""

    def __init__(self):
        """Initialize `id`, `created_at`, and `updated_at`."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Refresh the `updated_at` timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update any existing attributes from `data` (a dict),
        then call `save()` to refresh `updated_at`.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
