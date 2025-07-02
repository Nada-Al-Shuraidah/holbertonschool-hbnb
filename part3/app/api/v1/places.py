from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Models
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_output = api.model('PlaceOut', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model)),
    'reviews': fields.List(fields.Nested(review_model))
})

place_input = api.model('PlaceIn', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'amenities': fields.List(fields.String, required=True)
})

# Routes
@api.route('/')
class PlaceList(Resource):
    @api.marshal_list_with(place_output)
    def get(self):
        """Public: Get all places"""
        return [serialize_place(p) for p in facade.get_all_places()]

    @api.expect(place_input)
    @api.marshal_with(place_output, code=201)
    @jwt_required()
    def post(self):
        """Authenticated: Create new place"""
        payload = api.payload
        current_user = get_jwt_identity()
        payload['owner_id'] = current_user['id']  # Force ownership
        try:
            place = facade.create_place(payload)
            return serialize_place(place), 201
        except ValueError as ve:
            return {'error': str(ve)}, 400


@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_output)
    def get(self, place_id):
        """Public: Get place details"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return serialize_place(place)

    @api.expect(place_input)
    @jwt_required()
    def put(self, place_id):
        """Authenticated: Update owned place"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        if str(place.owner.id) != current_user['id']:
            return {'error': 'Unauthorized action'}, 403

        payload = api.payload
        try:
            updated = facade.update_place(place_id, payload)
            return {'message': 'Place updated successfully'}, 200
        except ValueError as ve:
            return {'error': str(ve)}, 400


# Serialization helper
def serialize_place(place):
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner': {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email
        },
        'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities],
        'reviews': [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user.id if r.user else None
            }
            for r in getattr(place, 'reviews', [])
        ]
    }
