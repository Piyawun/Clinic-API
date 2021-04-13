from re import T
from flask import request, jsonify, Response, jsonify, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.medicines import Medicine
from datetime import date

import time

class MedicineApi(Resource):

    def get(self) -> Response:
        medicine = Medicine.objects()
        if len(medicine) > 0:
            response = jsonify(medicine)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    def post(self) -> Response:

        schema = Kanpai.Object({
            'medicineID': Kanpai.String().required(),
            'name': Kanpai.String().required(),
            'amount': Kanpai.String().required(),
            'lot_num': Kanpai.String().required(),
            'MFG': Kanpai.String().required(),
            'EXP': Kanpai.String().required(),
            'price': Kanpai.String().required(),
            'create_at': Kanpai.String().required(),
            'update_at': Kanpai.String().required()
        })

        body = request.get_json()
        today = date.today()

        key = str(round(time.time()*999));
        data = {
            'medicineID': key,
            'name': body['name'],
            'amount': body['amount'],
            'lot_num': body['lot_num'],
            'MFG': body['MFG'],
            'EXP': body['EXP'],
            'price': body['price'],
            'create_at': str(today.strftime("%d/%m/%Y")),
            'update_at': str(today.strftime("%d/%m/%Y"))
        }

        validate_result =schema.validate(data)
        if validate_result.get('success', False) is False:
            print(data)
            return Response(status=400)

        try:

            Medicine(**data).save()
            return Response(status=201)
        
        except Exception as e:
            print(e)
            return Response("ID is already exit", status=400)


class MedicineApiID(Resource):

    # @jwt_required()
    def get(self) -> Response:
        body = request.get_json()
        patent = Medicine.objects(medicineID=body['medicineID'])
        if len(patent) > 0:
            response = jsonify(patent)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    def delete(self) -> Response:
        body = request.get_json()
        obj = Medicine.objects(medicineID=body['medicineID'])
        obj.delete()
        response = Response()
        response.status_code = 200
        
    def put(self)-> Response:
        today = date.today()
        body = request.get_json()
        patent = Medicine.objects(medicineID=body['medicineID'])
        if len(patent) > 0:
            Medicine.objects(medicineID=body['medicineID']).update(
                set__name=body['name'],
                set__amount=body['amount'],
                set__lot_num=body['lot_num'],
                set__MFG=body['MFG'],
                set__EXP=body['EXP'],
                set__price=body['price'],
                set__update_at=str(today.strftime("%d/%m/%Y")))
            response = Response("Success to updated medicine")
            response.status_code = 200
            return response
        else:
            return Response("No have medicineID", status=400)