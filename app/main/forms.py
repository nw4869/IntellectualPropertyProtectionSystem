import sys
from sha3 import keccak_256

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

import app
from app.models import File, Wallet


class UploadForm(FlaskForm):
    filename = StringField('名称', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('描述', validators=[Length(max=255)])
    file = FileField('文件', validators=[
        FileAllowed(app.upload_files, '不支持该文件类型'),
        FileRequired('文件未选择！')
    ])
    for_sell = BooleanField('是否展示和出售')
    price = FloatField('价钱(以太)', default=0)
    submit = SubmitField('上传')

    def validate_file(self, file_field):
        hash = keccak_256(file_field.data.stream.read()).hexdigest()
        # reset file index to start
        file_field.data.stream.seek(0)
        file = File.query.filter_by(hash=hash).first()
        if file:
            if file.owner_user == current_user:
                raise ValidationError('您已上传该作品')
            else:
                raise ValidationError('作品已有人上传')

    def validate_price(self, price_field):
        if price_field.data is None and self.for_sell.data:
            raise ValidationError('请输入价钱')
        else:
            NumberRange(min=0, max=sys.maxsize)(self, price_field)
        # if not current_user.wallets:
        #     raise ValidationError('没有以太坊钱包')
        # wallet = current_user.wallets[0]
        # if wallet.balance < price_field.data:
        #     raise ValidationError('余额不足')