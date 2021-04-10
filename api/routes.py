from flask_restful import Api
from api.authentication import SignUpAPI, TokenAPI, RefreshToken

def create_route(api:Api):
    # Authentication
    api.add_resource(SignUpAPI, '/authentication/signup')
    api.add_resource(TokenAPI, '/authentication/token')
    api.add_resource(RefreshToken, '/authentication/token/refresh')

