from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns  # تأكد من وجود هذا الملف والـ namespace

def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تهيئة JWTManager
    jwt = JWTManager(app)

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # تسجيل الـ namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')  # إضافة namespace الخاصة بالتوثيق

    print(app.url_map)
    return app
