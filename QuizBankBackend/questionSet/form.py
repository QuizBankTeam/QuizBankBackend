from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, DateField
from wtforms.validators import DataRequired, UUID
from QuizBankBackend.question.form import PostQuestionForm


class PostQuestionSetForm(FlaskForm):
    description = StringField(
        label='description',
        validators=[DataRequired()]
    )
    image = FieldList(StringField(
        validators=[DataRequired()]
    ))
    questionBank = StringField(
        label='questionBank',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    questions = FieldList(FormField(PostQuestionForm))
    createdDate = DateField(
        label='createdDate',
        validators=[DataRequired()]
    )
    originateFrom = StringField(
        label='originateFrom',
        validators=[
            DataRequired(),
            UUID()
        ]
    )

class PutQuestionSetForm(FlaskForm):
    questionSetId = StringField(
        label='questionSetId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    description = StringField(
        label='description',
        validators=[DataRequired()]
    )
    image = FieldList(StringField(
        validators=[DataRequired()]
    ))
    questions = FieldList(FormField(PostQuestionForm))


class MoveQuestionSetForm(FlaskForm):
    questionSetId = StringField(
        label='questionSetId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    newBankId = StringField(
        label='newBankId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )