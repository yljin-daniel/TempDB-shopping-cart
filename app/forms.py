from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class LoginForm(Form):

    userid = StringField('User ID:', [validators.InputRequired('Userid required')])
    password = PasswordField('Password:', [validators.InputRequired('Password required')])


class CustomerRegForm(Form):

    userid = StringField('User ID:', [validators.InputRequired('Userid required')])
    name = StringField('Name:', [validators.DataRequired('Name required')])
    password = PasswordField('Password:', [validators.InputRequired('Password required')])
    password2 = PasswordField('Re-enter Password:', [validators.EqualTo('password', message='Passwords are different')])

    #Regex for date validation MM/DD/YYYY MM/DD/YY
    reg_date = r'\A(?:(?:(?:(?:0?[13578])|(1[02]))/31/(19|20)?\d\d)|(?:(?:(?:0?[13-9])|(?:1[0-2]))/(?:29|30)/(?:19|20)?\d\d)|(?:0?2/29/(?:19|20)(?:(?:[02468][048])|(?:[13579][26])))|(?:(?:(?:0?[1-9])|(?:1[0-2]))/(?:(?:0?[1-9])|(?:1\d)|(?:2[0-8]))/(?:19|20)?\d\d))\Z'
    birthday = StringField('BirthDate:', [validators.Regexp(reg_date, message='Invalid Date input')])
    address = StringField('Address:')
    phone = StringField('Tel:')
