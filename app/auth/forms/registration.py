from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp


class RegistrationForm(FlaskForm):
    email = StringField(
       'E-mail',
        validators=[DataRequired(), Email()],
    )
    firstname = StringField('First Name', validators=[DataRequired()],)
    lastname = StringField('Last Name',)
    username = StringField(
        'Username',
        validators=[Regexp(r'^[a-zA-Z0-9_]{5,30}$',
                           message='Username should include english letters, numeric digits and symbol "_" only. '
                                      'Also it should contains al lest 5 symbols and not more than 30.')],
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Regexp(
                r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{6,20})',
                message='Notice - password should contains lowercase, uppercase, digit and special symbols'
            ),
        ],
    )
    submit = SubmitField('Registration')
