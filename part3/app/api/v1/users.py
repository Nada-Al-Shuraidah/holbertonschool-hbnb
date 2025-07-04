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
        """Register a new user (public registration)"""
        payload = api.payload
        if facade.get_user_by_email(payload['email']):
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(payload)
        return new_user.to_dict(), 201


@api.route('/admin')
class AdminUserCreate(Resource):
    @api.expect(create_user_model, validate=True)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Admin: Create a new user"""
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403

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
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update user details (admin can modify anything, user can't update email/password)"""
        identity = get_jwt_identity()
        is_admin = identity.get("is_admin", False)
        is_owner = user_id == identity["id"]

        if not is_admin and not is_owner:
            return {'error': 'Unauthorized action'}, 403

        payload = api.payload

        # Check email uniqueness if it's being changed
        if 'email' in payload:
            existing = facade.get_user_by_email(payload['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Only admin can change email or password
        if not is_admin and ('email' in payload or 'password' in payload):
            return {'error': 'You cannot modify email or password.'}, 400

        updated = facade.update_user(user_id, payload)
        if not updated:
            api.abort(404, 'User not found')
        return updated.to_dict()
