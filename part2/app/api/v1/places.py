from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

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
    'reviews': fields.List(fields.Nested(review_model))  # ✅ تمت الإضافة هنا
})

place_input = api.model('PlaceIn', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String, required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input)
    @api.marshal_with(place_output, code=201)
    def post(self):
        try:
            place = facade.create_place(api.payload)
            return serialize_place(place), 201
        except ValueError as ve:
            return {'error': str(ve)}, 400

    @api.marshal_list_with(place_output)
    def get(self):
        return [serialize_place(p) for p in facade.get_all_places()]

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_output)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")
        return serialize_place(place)

    @api.expect(place_input)
    def put(self, place_id):
        try:
            updated = facade.update_place(place_id, api.payload)
            if not updated:
                api.abort(404, "Place not found")
            return {'message': 'Place updated successfully'}, 200
        except ValueError as ve:
            return {'error': str(ve)}, 400

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
