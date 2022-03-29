from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class RegistrationForm(Form):
    userid = StringField('User ID:', [validators.DataRequired('type ID')])
    username = StringField('Username:', [validators.DataRequired('type username')])
    password = PasswordField('Password:', [validators.DataRequired('type password')])
    password2 = PasswordField('Repeat Password:', [validators.EqualTo('password', message='Password not match')])
    email = StringField('Email:', [validators.DataRequired('type email'), validators.Email('Invalid Email')])
    phone = StringField('Phone:', [validators.DataRequired('type phone number')])
    address = StringField('Address:', [validators.DataRequired('type address')])

class LoginForm(Form):

    userid = StringField('User ID:', [validators.InputRequired('Userid required')])
    password = PasswordField('Password:', [validators.InputRequired('Password required')])