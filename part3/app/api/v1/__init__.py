from flask_restx import Api

api = Api()

from .auth import api as auth_ns
from .users import api as users_ns

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')
