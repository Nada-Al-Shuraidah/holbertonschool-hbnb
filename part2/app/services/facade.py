# app/services/facade.py

from app.models.user import User
from app.persistence.repository import InMemoryRepository   # ← fixed import
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        # now using your InMemoryRepository from persistence/repository.py
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Only whitelist these fields
        for field in ('first_name', 'last_name', 'email'):
            if field in data:
                setattr(user, field, data[field])

        # Persist by re-adding (overwrites in-memory)
        self.user_repo.add(user)
        return user
        

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            if len(amenity_data['name']) > 50:
                raise ValueError("Name must be 50 characters or fewer.")
            amenity.name = amenity_data['name']

        self.amenity_repo.add(amenity)
        return amenity
