import time
import uuid
from datetime import datetime

from flask import request, jsonify, Response, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from mongoengine import *
from kanpai import Kanpai

from models.reports import Reports
from models.bookings import Bookings


class ReportAPI(Resource):

    def post(self) -> Response:
        body = request.get_json()
        booking = Bookings.objects(bookingID=body['bookingID'])
        print(len(booking))
        if len(booking) > 0:
            schema = Kanpai.Object({
                'reportID': Kanpai.String().required(),
                'bookingID': Kanpai.String().required(),
                'staffID': Kanpai.String().required(),
                'patentID': Kanpai.String().required(),
                'header': Kanpai.String().required(),
                'detail': Kanpai.String().required(),
                'create_at': Kanpai.String(),
                'update_at': Kanpai.String()
            })

            key = uuid.uuid4().int
            data = {
                'reportID': str(key)[0:6] + '_' + body['patentID'],
                'bookingID': body['bookingID'],
                'staffID': body['staffID'],
                'patentID': body['patentID'],
                'header': body['header'],
                'detail': body['detail'],
                'create_at': str(datetime.utcnow()),
                'update_at': str(datetime.utcnow())
            }

            validate_result = schema.validate(data)
            if validate_result.get('success', False) is False:
                return Response(status=400)

            try:
                Bookings.objects(bookingID=body['bookingID']).update(
                    set__status="ตรวจเสร็จสิ้น",
                    set__update_at=str(datetime.utcnow())
                )

                Reports(**data).save()
                return Response(status=201)

            except NotUniqueError:
                return Response("Report is already add to storage", status=400)
        else:
            return Response("Report number don't match", status=400)

    # Get all report
    def get(self) -> Response:
        report = Reports.objects()
        if len(report) > 0:
            response = jsonify(report)
            response.status_code = 200
            return response

        else:
            response = Response()
            response.status_code = 204
            return response


class ReportIdAPI(Resource):

    def get(self) -> Response:
        body = request.get_json()
        id = body['reportID']

        pipline = [
            {"$match": {"_id": id}},
            {"$lookup":
                 {'from': 'bookings', 'localField': 'bookingID', 'foreignField': '_id', 'as': 'bookings'}
             },
            {"$lookup":
                 {'from': 'users', 'localField': 'staffID', 'foreignField': '_id', 'as': 'staffs'}
             },
            {"$lookup":
                 {'from': 'patients', 'localField': 'patentID', 'foreignField': '_id', 'as': 'patients'}
             }
        ]

        report = Reports.objects.aggregate(pipline)
        x = list(report)
        y = list(x)

        if len(y) > 0:
            staff = y[0]['staffs']
            patient = y[0]['patients']
            booking = y[0]['bookings']
            data = {
                'reportID': y[0]['_id'],
                'booking': booking[0],
                'patient': patient[0],
                'staff': {
                    '_id': staff[0]['_id'],
                    'name': staff[0]['name'],
                    'role': staff[0]['role'],
                    'department': staff[0]['department']
                },
                'report': {
                    '_id': y[0]['header'],
                    'detail': y[0]['detail'],
                    'create_at': y[0]['create_at'],
                    'update_at': y[0]['update_at']
                }

            }
            response = jsonify(data)
            response.status_code = 200
            return response
        else:
            response = Response()
            response.status_code = 204
            return response

    def delete(self) -> Response:
        body = request.get_json()
        reportObj = Reports.objects(reportID=body['reportID'])
        if len(reportObj) > 0:
            reportObj.delete()
            response = Response()
            response.status_code = 200
        else:
            return Response(status=204)


def put(self) -> Response:
    body = request.get_json()
    report = Reports.objects(reportID=body['reportID'])
    if len(report) > 0:
        Reports.objects(reportID=body['reportID']).update(
            set__header=body['header'],
            set__detail=body['detail'],
            set__update_at=str(datetime.utcnow()))
        response = Response("Success to updated report")
        response.status_code = 200
        return response
    else:
        return Response("No have booking", status=204)