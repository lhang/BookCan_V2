#! -*- coding: utf-8 -*-


from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    email = TextField('email')
    passwd = PasswordField('passwd')
    remember_me = BooleanField('remember_me')


class CanForm(Form):
    name = TextField('name')
    intro = TextAreaField('intro')


class RegistForm(Form):
    name = TextField('name')
    passwd = PasswordField('passwd')
    email = TextField('email')


class BookForm(Form):
    name = TextField('name')
    intro = TextAreaField('intro')
    link = TextField('link')


class MeaageForm(Form):
    content = TextField('content')
