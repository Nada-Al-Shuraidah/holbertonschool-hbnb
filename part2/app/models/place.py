from .base_model import BaseModel
from .user       import User

class Place(BaseModel):
    """A rental property listing, owned by a User."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        # Validate owner relation
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance.")

        # Assign attributes (with simple truncation for title)
        self.title       = title[:100]
        self.description = description
        self.price       = float(price)
        self.latitude    = float(latitude)
        self.longitude   = float(longitude)
        self.owner       = owner

        # Prepare containers for related objects
        self.reviews   = []
        self.amenities = []

    def add_review(self, review):
        """Add a Review object to this Place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an Amenity object to this Place."""
        self.amenities.append(amenity)

    def display_reviews(self):
        """
        Display all reviews for this place.
        """
        if not self.reviews:
            print("There are no reviews for this place.")
            return

        for review in self.reviews:
            print(f"{review.user.first_name}: {review.text}")

    def display_amenities(self):
        """
        Display all amenities associated with this place.
        """
        if not self.amenities:
            print("There are no amenities in this place.")
            return

        print("Amenities:")
        for amenity in self.amenities:
            print(f" - {amenity.name}")
