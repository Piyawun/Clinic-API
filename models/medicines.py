from mongoengine import Document,StringField,DateTimeField,DecimalField
from datetime import date


class Medicine(Document):
    medicineID = StringField(required=True,unique=True)
    name = StringField(required=True)
    amount = DecimalField(required=True,default=0,MinValue=0, rounding='ROUND_HALF_UP')
    lot_num = StringField(required=True)
    MFG = StringField(required=True)
    EXP = StringField(required=True,NotNull=True)
    price = DecimalField(required=True,default=0,MinValue=0, rounding='ROUND_HALF_UP')
    create_at = StringField(required=False)
    update_at = StringField(required=False)