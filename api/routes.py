from flask_restful import Api
from api.authentication import SignUpAPI, TokenAPI, RefreshToken

from api.patent import PatentApi,PatentApiID
from api.medicine import MedicineApi,MedicineApiID

def create_route(api: Api):
    # Authentication
    api.add_resource(SignUpAPI, '/authentication/signup')
    api.add_resource(TokenAPI, '/authentication/token')
    api.add_resource(RefreshToken, '/authentication/token/refresh')

    api.add_resource(PatentApi, '/patent')
    api.add_resource(PatentApiID, '/patent/id')

    api.add_resource(MedicineApi, '/medicine')
    api.add_resource(MedicineApiID, '/medicine/id')
