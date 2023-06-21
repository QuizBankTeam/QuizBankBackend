from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField
from wtforms.validators import DataRequired, UUID
from QuizBankBackend.questionBank.form import QUESTION_BANK_TYPE


class GetQuestionForm(FlaskForm):
    class Meta:
        csrf = False

    questionId = StringField(
        label='questionId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )


QUESTION_TYPE = ['Filling', 'MultipleChoiceS',
                 'ShortAnswer', 'MultipleChoiceM', 'TrueOrFalse']


class PostQuestionForm(FlaskForm):
    title = StringField(
        label='title',
        validators=[DataRequired()]
    )
    number = StringField(
        label='number',
        validators=[DataRequired()]
    )
    description = StringField(
        label='description',
        validators=[DataRequired()]
    )
    options = FieldList(StringField(
        validators=[DataRequired()]
    ))
    questionType = SelectField(
        label='questionType',
        choices=QUESTION_TYPE
    )
    bankType = SelectField(
        label='bankType',
        choices=QUESTION_BANK_TYPE
    )
    questionBank = StringField(
        label='questionBank',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    answerOptions = FieldList(StringField(
        validators=[DataRequired()]
    ))
    answerDescription = StringField(
        label='answerDescription',
        validators=[DataRequired()]
    )
    provider = StringField(
        label='provider',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    originateFrom = StringField(
        label='originateFrom',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    createdDate = DateField(
        label='createdDate',
        validators=[DataRequired()]
    )
    image = FieldList(StringField(
        validators=[DataRequired()]
    ))
    tag = FieldList(StringField(
        validators=[DataRequired()]
    ))


class PutQuestionForm(PostQuestionForm):
    questionId = StringField(
        label='questionId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )


class DeleteQuestionForm(GetQuestionForm):
    class Meta:
        csrf = True
