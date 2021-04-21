from flask import request, Response, jsonify, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.patients import Patients
from datetime import date

import time


class PatentApi(Resource):
    # @jwt_required()
    def get(self) -> Response:
        patent = Patients.objects()
        if len(patent) > 0:
            response = jsonify(patent)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    # @jwt_required()
    def post(self) -> Response:
        schema = Kanpai.Object({
            'patentID': Kanpai.String().required(),
            'name': Kanpai.String().required(),
            'dob': Kanpai.String().required(),
            'tel': Kanpai.String().required(),
            'email': Kanpai.Email().required(),
            'job': Kanpai.String().required(),
            'create_at': Kanpai.String().required(),
            'update_at': Kanpai.String().required()
        })

        body = request.get_json()
        today = date.today()

        key = str(round(time.time() * 999))
        data = {
            'patentID': key,
            'name': body['name'],
            'dob': body['dob'],
            'tel': body['tel'],
            'email': body['email'],
            'job': body['job'],
            'create_at': str(today.strftime("%d/%m/%Y")),
            'update_at': str(today.strftime("%d/%m/%Y"))
        }

        validate_result = schema.validate(data)
        if validate_result.get('success', False) is False:
            return Response(status=400)

        try:
            Patients(**data).save()
            return Response(status=201)

        except NotUniqueError:
            return Response("Name is already exit", status=400)


class PatentApiID(Resource):

    # @jwt_required()
    def get(self) -> Response:
        body = request.get_json()
        patent = Patients.objects(patentID=body['patentID'])
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
        obj = Patients.objects(patentID=body['patentID'])
        obj.delete()
        response = Response()
        response.status_code = 200

    def put(self) -> Response:
        today = date.today()
        body = request.get_json()
        patent = Patients.objects(patentID=body['patentID'])
        if len(patent) > 0:
            obj = Patients.objects(patentID=body['patentID']).update(set__name=body['name'], set__dob=body['dob'],
                                                                     set__tel=body['tel'], set__email=body['email'],
                                                                     set__job=body['job'],
                                                                     set__update_at=str(today.strftime("%d/%m/%Y")))
            response = Response("Success to updated patent")
            response.status_code = 200
            return response
        else:
            return Response("No have parentID", status=400)
