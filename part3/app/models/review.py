from .base_model import BaseModel
from .place      import Place
from .user       import User

class Review(BaseModel):
    """A user’s feedback on a specific place."""

    def __init__(self, text, rating, place, user):
        super().__init__()

        # Validate related objects
        if not isinstance(place, Place):
            raise TypeError("Place must be a Place instance.")
        if not isinstance(user, User):
            raise TypeError("User must be a User instance.")

        # Validate rating
        val = int(rating)
        if not 1 <= val <= 5:
            raise ValueError("Rating must be an integer between 1 and 5.")

        # Assign attributes
        self.text   = text
        self.rating = val
        self.place  = place
        self.user   = user
