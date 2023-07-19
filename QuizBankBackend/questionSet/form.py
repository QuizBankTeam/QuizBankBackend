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

class PutQuestionSetForm(PostQuestionSetForm):
    questionSetId = StringField(
        label='questionSetId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )