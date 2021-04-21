from flask_restful import Api
from api.authentication import SignUpAPI, TokenAPI, RefreshToken, getUserByIdAPI, getUserAPI

from api.patent import PatentApi, PatentApiID
from api.medicine import MedicineApi, MedicineApiID
from api.booking import BookingApi, BookingApiID
from api.payment import PaymentApi, PaymentIdAPI
from api.report import ReportAPI, ReportIdAPI
from api.dispense import DispenseApi
from api.order import OrderApi, SearchOrderByReport


def create_route(api: Api):
    # Authentication
    api.add_resource(SignUpAPI, '/authentication/signup')
    api.add_resource(TokenAPI, '/authentication/token')
    api.add_resource(RefreshToken, '/authentication/token/refresh')

    # Patent ระบบการเพิ่มผู่ป่วย
    api.add_resource(PatentApi, '/patent')
    api.add_resource(PatentApiID, '/patent/id')

    # Medicine ระบบยา
    api.add_resource(MedicineApi, '/medicine')
    api.add_resource(MedicineApiID, '/medicine/id')

    # Booking จัดการ ตารางการจอง
    api.add_resource(BookingApi, '/booking')
    api.add_resource(BookingApiID, '/booking/id')

    # staff ผู้ดูแล หมอ พญาบาล
    api.add_resource(getUserByIdAPI, '/user/id')
    api.add_resource(getUserAPI, '/user')

    # Report รายงานประวัติผู้ป่วย
    api.add_resource(ReportAPI, '/report')
    api.add_resource(ReportIdAPI, '/report/id')

    # dispense จ่ายยา
    api.add_resource(DispenseApi, '/dispense')

    # Order
    api.add_resource(OrderApi, '/orders')
    api.add_resource(SearchOrderByReport, '/orders/report')

    # PaymentAPI
    api.add_resource(PaymentApi, '/payments')
    api.add_resource(PaymentIdAPI,'/payments/id')
