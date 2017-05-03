from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 255)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 255)])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')

    next = HiddenField('next')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 255)])
    name = StringField('姓名', validators=[DataRequired(), Length(1, 255)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 255)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 255)])
    re_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', '两个密码需要一致'), Length(1, 255)])
    submit = SubmitField('注册')

    next = HiddenField('next')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经注册')
