import uuid
from datetime import datetime

from flask import request, jsonify, Response, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.orders import Orders


class OrderApi(Resource):

    def post(self) -> Response:
        body = request.get_json()
        schema = Kanpai.Object({
            'orderID': Kanpai.String().required(),
            'reportID': Kanpai.String().required(),
            'subject': Kanpai.String().required(),
            'price': Kanpai.String().required(),
            'staffID': Kanpai.String().required(),
            'create_at': Kanpai.String(),
            'update_at': Kanpai.String()
        })

        key = uuid.uuid4().int
        data = {
            'orderID': str(key)[0:6],
            'reportID': body['reportID'],
            'subject': body['subject'],
            'price': body['price'],
            'staffID': body['staffID'],
            'create_at': str(datetime.utcnow()),
            'update_at': str(datetime.utcnow())
        }

        validate_result = schema.validate(data)
        if validate_result.get('success', False) is False:
            return Response(status=400)

        try:
            Orders(**data).save()
            response = jsonify(data)
            response.status_code = 200
            return response

        except NotUniqueError:
            return Response(status=400)

    def get(self) -> Response:
        body = request.get_json()
        id = body['orderID']
        order = Orders.objects(orderID=id)
        if len(order) > 0:
            response = jsonify(order)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    def delete(self) -> Response:
        body = request.get_json()
        id = body['orderID']
        order = Orders.objects(oderID=id)
        if len(order) > 0:
            order.delete()
            return Response(status=200)
        else:
            response = Response()
            response.status_code = 204
            return response


class SearchOrderByReport(Resource):

    def get(self) -> Response:
        body = request.get_json()
        id = body['reportID']
        order = Orders.objects(reportID=id)
        if len(order) > 0:
            response = jsonify(order)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response
