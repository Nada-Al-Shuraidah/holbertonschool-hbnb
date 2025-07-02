from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='Amenity unique identifier'),
    'name': fields.String(required=True, description='Name of the amenity')
})

create_amenity_model = api.model('CreateAmenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(create_amenity_model)
    @api.marshal_with(amenity_model, code=201)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            new_amenity = facade.create_amenity(api.payload)
            return new_amenity, 201
        except ValueError as ve:
            return {'error': str(ve)}, 400

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities()


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')
        return amenity

    @api.expect(create_amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            updated = facade.update_amenity(amenity_id, api.payload)
            if not updated:
                api.abort(404, 'Amenity not found')
            return {'message': 'Amenity updated successfully'}, 200
        except ValueError as ve:
            return {'error': str(ve)}, 400
