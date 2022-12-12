from flask_wtf import FlaskForm

from wtforms import SubmitField, PasswordField, HiddenField
from wtforms.validators import DataRequired, EqualTo


class ResetPasswordForm(FlaskForm):
    token = HiddenField('Reset')
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message="Passwords must match")])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Submit')

    def set_token(self, token):
        self.token.data = token
