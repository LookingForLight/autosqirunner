#-*-coding:utf-8-*-
from flask_wtf import FlaskForm
from wtforms import validators, fields, widgets

class MyForm(FlaskForm):
    Username = fields.StringField(
        label='用户名1',
        validators=[
            validators.DataRequired(message='用户名不能为空'),
            validators.length(min=6, max=11, message='用户名长度必须大于%(min)d且小于%(max)d')
        ],
        widget=widgets.TextInput(),
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入用户名1',
            'required': '',
            'autofocus': ''
            }
    )
    Password = fields.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空'),
            validators.length(min=6, message='密码必须大于%(min)d位')
        ],
        widget=widgets.PasswordInput(),
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'required': '',
            'autofocus': ''
        }
    )


class AutosqliForm(FlaskForm):

    test_url = fields.StringField(

        label="TEST URL:",
        validators = [
            validators.DataRequired(message='URL不能为空'),
            validators.URL(require_tld=False,message='url不正确')
        ]
    )