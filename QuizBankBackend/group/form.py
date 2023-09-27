from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, DateField, FormField
from wtforms.validators import DataRequired, UUID, Optional


class PostChatroomForm(FlaskForm):
    name = StringField(
        label='name',
        validators=[
            DataRequired()
        ]
    )
    avatar = StringField(
        label='avatar',
        validators=[
            Optional()
        ]
    )
    createdDate = DateField(
        label='createdDate',
        validators=[
            DataRequired()
        ]
    )

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
    chatroom = FormField(PostChatroomForm)
    questionBanks = FieldList(StringField(
        validators=[
            DataRequired(),
            UUID()
        ]
    ))

class PutGroupForm(FlaskForm):
    groupId = StringField(
        label='groupId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
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
    questionBanks = FieldList(StringField(
        validators=[
            DataRequired(),
            UUID()
        ]
    ))
