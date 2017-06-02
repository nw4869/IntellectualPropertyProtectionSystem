from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, FloatField, ValidationError, SubmitField
from wtforms.validators import NumberRange
import sys

from app import ethereum_service


class TransferForm(FlaskForm):
    to = StringField('to')
    value = FloatField('value')
    submit = SubmitField('submit')

    def validate_to(self, filed):
        if not ethereum_service.is_address(filed.data):
            raise ValidationError('地址有误')

    def validate_value(self, field):
        try:
            self.validate_to(self.to)
        except ValidationError:
            return

        NumberRange(min=0, max=sys.maxsize, message='金额有误')(self, field)

        address = current_user.wallets[0].address
        money_wei = ethereum_service.to_wei(field.data)
        balance = ethereum_service.get_balance(address)
        estimate_wei = ethereum_service.estimate_tx_wei({'from': address, 'to': self.to.data})
        if balance < money_wei + estimate_wei:
            raise ValidationError('余额不足')
