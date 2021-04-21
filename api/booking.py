from re import T
from flask import request, jsonify, Response, jsonify, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import NotUniqueError, DoesNotExist
from kanpai import Kanpai

from models.bookings import Bookings
from datetime import date, datetime

import time


class BookingApi(Resource):

    def get(self) -> Response:
        booking = Bookings.objects()
        if len(booking) > 0:
            response = jsonify(booking)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    def post(self) -> Response:

        schema = Kanpai.Object({
            'bookingID': Kanpai.String().required(),
            'staffID': Kanpai.String().required(),
            'patentID': Kanpai.String().required(),
            'detail': Kanpai.String().required(),
            'dateBooking': Kanpai.String().required(),
            'status': Kanpai.String().required(),
            'create_at': Kanpai.String().required(),
            'update_at': Kanpai.String().required()
        })

        body = request.get_json()

        key = str(round(time.time() * 999))
        data = {
            'bookingID': key,
            'staffID': body['staffID'],
            'patentID': body['patentID'],
            'detail': body['detail'],
            'dateBooking': body['dateBooking'],
            'status': body['status'],
            'create_at': str(datetime.utcnow()),
            'update_at': str(datetime.utcnow())
        }

        validate_result = schema.validate(data)
        if validate_result.get('success', False) is False:
            return Response(status=400)

        try:

            Bookings(**data).save()
            return Response(status=201)

        except NotUniqueError:
            return Response("ID is already exit", status=400)


class BookingApiID(Resource):

    # @jwt_required()
    def get(self) -> Response:
        body = request.get_json()
        booking = Bookings.objects(bookingID=body['bookingID'])
        if len(booking) > 0:
            response = jsonify(booking)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    def delete(self) -> Response:
        body = request.get_json()
        obj = Bookings.objects(bookingID=body['bookingID'])
        obj.delete()
        response = Response()
        response.status_code = 200

    def put(self) -> Response:

        body = request.get_json()
        booking = Bookings.objects(bookingID=body['bookingID'])
        if len(booking) > 0:
            Bookings.objects(bookingID=body['bookingID']).update(
                set__dateBooking=body['dateBooking'],
                set__status=body['status'],
                set__update_at=str(datetime.utcnow()))
            response = Response("Success to updated booking")
            response.status_code = 200
            return response
        else:
            return Response("No have booking", status=400)
