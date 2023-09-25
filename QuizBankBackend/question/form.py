from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField
from wtforms.validators import DataRequired, UUID, Optional
from QuizBankBackend.constant import *


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
    questionImage = FieldList(StringField(
        validators=[DataRequired()]
    ))
    answerImage = FieldList(StringField(
        validators=[DataRequired()]
    ))
    tag = FieldList(StringField(
        validators=[DataRequired()]
    ))

class PutQuestionForm(FlaskForm):
    questionId = StringField(
        label='questionId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
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
    answerOptions = FieldList(StringField(
        validators=[DataRequired()]
    ))
    answerDescription = StringField(
        label='answerDescription',
        validators=[DataRequired()]
    )
    questionImage = FieldList(StringField(
        validators=[DataRequired()]
    ))
    answerImage = FieldList(StringField(
        validators=[DataRequired()]
    ))
    tag = FieldList(StringField(
        validators=[DataRequired()]
    ))

class PatchAnswerForm(FlaskForm):
    questionId = StringField(
        label='questionId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    questionSetId = StringField(
        label='questionSetId',
        validators=[
            Optional(),
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

class PatchTagForm(FlaskForm):
    questionId = StringField(
        label='questionId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    questionSetId = StringField(
        label='questionSetId',
        validators=[
            Optional(),
            UUID()
        ]
    )
    tag = FieldList(StringField(
        validators=[DataRequired()]
    ))

class MoveQuestionForm(FlaskForm):
    questionId = StringField(
        label='questionId',
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