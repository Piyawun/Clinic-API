from flask import Flask
from flask_cors import CORS
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restful import Api

from flask_pymongo import pymongo
from flask_mongoengine import MongoEngine

from api.routes import create_route



config = {
    'JSON_SORT_KEYS': False,
    'MONGODB_SETTINGS': {
        'host':'mongodb+srv://clinicDB:Clinic2543@clinicm.amrfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    },
    'JWT_SECRET_KEY': '&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdSg',
    'JWT_ACCESS_TOKEN_EXPIRES': 300,
    'JWT_REFRESH_TOKEN_EXPIRES': 604800
}

# init flask
app = Flask(__name__)

# configure app
app.config.update(config)

# init api and routes
api = Api(app)
create_route(api=api)

# init MongoEngine
db = MongoEngine(app=app)

# init jwt manager
jwt = JWTManager(app=app)

# setup CORS
CORS(app, resources={r"/*": {"origin": "*"}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=True)
