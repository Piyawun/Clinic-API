from flask import Flask
from flask_cors import CORS
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from api.routes import create_route


app = Flask(__name__)
config = {
    'JSON_SORT_KEYS': False,
    'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:2543@localhost:5432/Clinic',
    'SECRET_KEY':'this-really-needs-to-be-changed',
    'JWT_SECRET_KEY': '&F)J@NcRfUjXn2r5u7x!A%D*G-KaPdSg',
    'JWT_ACCESS_TOKEN_EXPIRES': 300,
    'JWT_REFRESH_TOKEN_EXPIRES': 604800
}

db = SQLAlchemy(app)

# init api and routes
api = Api(app)
create_route(api=api)


migrate = Migrate(app, db)

# init jwt manager
jwt = JWTManager(app=app)

# setup CORS
CORS(app, resources={r"/*": {"origin": "*"}})


if __name__ == '__main__':
    app.run(debug=True,reload=True)