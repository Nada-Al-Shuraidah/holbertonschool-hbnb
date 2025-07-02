from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Output model (excludes password)
user_model = api.model('User', {
    'id': fields.String(readOnly=True, description='User unique identifier'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
})

# Input model (includes password)
create_user_model = api.model('CreateUser', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users]

    @api.expect(create_user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        payload = api.payload
        if facade.get_user_by_email(payload['email']):
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(payload)
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
        return user.to_dict()

    @api.expect(create_user_model, validate=True)
    @api.marshal_with(user_model)
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details (only own account, no email/password)"""
        current_user = get_jwt_identity()
        if user_id != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        if 'email' in api.payload or 'password' in api.payload:
            return {'error': 'You cannot modify email or password.'}, 400

        updated = facade.update_user(user_id, api.payload)
        if not updated:
            api.abort(404, 'User not found')
        return updated.to_dict()
