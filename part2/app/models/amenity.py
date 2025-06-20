from .base_model import BaseModel

class Amenity(BaseModel):
    """An extra feature or service (for example, Wi-Fi)."""

    def __init__(self, name):
        super().__init__()

        # Validate name length
        if len(name) > 50:
            raise ValueError("Name must be 50 characters or fewer.")

        # Assign attribute
        self.name = name
