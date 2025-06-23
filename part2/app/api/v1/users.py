from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Expanded the model to include the read-only 'id' field
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='User unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
})

# Separate “create” model so we don’t require an 'id' on input
create_user_model = api.model('CreateUser', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        # Calls a facade method you’ll need to implement:
        # def get_all_users(self) -> List[User]
        return facade.get_all_users()

    @api.expect(create_user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        payload = api.payload

        # Reuse your existing facade method to check uniqueness
        if facade.get_user_by_email(payload['email']):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(payload)
        # facade.create_user must save the user and return the User object
        return new_user.to_dict(), 201

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user

    @api.expect(create_user_model, validate=True)
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details"""
        data = api.payload

        # Delegate to the facade so it can whitelist fields and persist:
        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            api.abort(404, 'User not found')

        return updated
