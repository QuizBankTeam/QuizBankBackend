from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField
from wtforms.validators import DataRequired, UUID, Optional


class PostGroupForm(FlaskForm):
    avatar = StringField(
        label='avatar',
        validators=[
            Optional()
        ]
    )
    name = StringField(
        label='name',
        validators=[
            DataRequired()
        ]
    )
    createdDate = DateField(
        label='createdDate',
        validators=[
            DataRequired()
        ]
    )
    members = FieldList(StringField(
        validators=[DataRequired()]
    ))
    questionBanks = FieldList(StringField(
        validators=[
            DataRequired(),
            UUID()
        ]
    ))
