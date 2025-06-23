# app/services/facade.py

from app.models.user import User
from app.persistence.repository
class HBnBFacade:
    def __init__(self):
        # our “database”
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Create a new User object, persist it, and return it.
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a single user by its ID (or return None if not found).
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Find a user by their email address (for uniqueness checks).
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Return a list of all users.
        Used by GET /api/v1/users/.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """
        Update only the allowed fields on an existing user,
        persist the changes, and return the updated user.
        Returns None if no user with that ID exists.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Whitelist updates
        for field in ('first_name', 'last_name', 'email'):
            if field in data:
                setattr(user, field, data[field])

        # Persist the updated object
        self.user_repo.add(user)
        return user
