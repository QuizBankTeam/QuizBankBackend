from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, UUID


class GetUserForm(FlaskForm):
    class Meta:
        csrf = False

    userId = StringField(
        label='userId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )


class RegisterForm(FlaskForm):
    username = StringField(
        label='username',
        validators=[DataRequired()]
    )
    email = EmailField(
        label='email',
        validators=[DataRequired()]
    )
    password = PasswordField(
        label='password',
        validators=[DataRequired()]
    )

class LoginForm(FlaskForm):
    username = StringField(
        label='username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        label='password',
        validators=[DataRequired()]
    )