from flask_wtf import FlaskForm

from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, Regexp


class LoginForm(FlaskForm):
    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField('Log In')
