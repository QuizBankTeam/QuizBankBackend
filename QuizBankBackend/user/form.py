from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, DateField
from wtforms.validators import DataRequired, UUID, Email


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
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        label='password',
        validators=[DataRequired()]
    )
    createdDate = DateField(
        label='createdDate',
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

class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        label='password',
        validators=[DataRequired()]
    )
    newPassword = PasswordField(
        label='newPassword',
        validators=[DataRequired()]
    )
    confirmNewPassword = PasswordField(
        label='confirmNewPassword',
        validators=[DataRequired()]
    )

class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        label='email',
        validators=[
            DataRequired(),
            Email()
        ]
    )