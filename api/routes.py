from flask_restful import Api
from api.authentication import SignUpApi, TokenApi, RefreshTokenApi

def create_route(api:Api):
    # Authentication
    api.add_resource(SignUpApi,'/authentication/signup')
    api.add_resource(TokenApi, '/authentication/token')
    api.add_resource(RefreshTokenApi, '/authentication/token/refresh')

