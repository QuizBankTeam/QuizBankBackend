from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField, FormField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, UUID
from QuizBankBackend.constant import *


class CopyQuestionForm(FlaskForm):
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
    bankType = StringField(
        label='bankType',
        validators=[DataRequired()]
    )
    questionBank = StringField(
        label='questionBank',
        validators=[
            DataRequired()
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
    answerImage = FieldList(StringField(
        validators=[DataRequired()]
    ))
    questionImage = FieldList(StringField(
        validators=[DataRequired()]
    ))
    tag = FieldList(StringField(
        validators=[DataRequired()]
    ))

class PostQuestionRecordForm(FlaskForm):
    user = StringField(
        label='user',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    userAnswerOptions = FieldList(
        StringField(
            label='userAnswerOptions',
            validators=[DataRequired()])
    )
    userAnswerDescription = StringField(
        label='userAnswer',
        validators=[DataRequired()]
    )
    correct = BooleanField(
        label='correct',
        validators=[DataRequired()],
        false_values={}
    )
    date = DateField(
        label='date',
        validators=[DataRequired()]
    )
    question = FormField(CopyQuestionForm)

class PostQuizRecordForm(FlaskForm):
    title = StringField(
        label='title',
        validators=[DataRequired()]
    )
    quizId = StringField(
        label='quizId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    type = SelectField(
        label='type',
        choices=QUIZ_TYPE
    )
    totalScore = IntegerField(
        label='totalScore',
        validators=[DataRequired()]
    )
    duringTime = IntegerField(
        label='duringTime',
        validators=[DataRequired()]
    )
    startDateTime = DateTimeField(
            label='startDateTime',
            validators=[DataRequired()]
        )
    endDateTime = DateTimeField(
        label='endDateTime',
        validators=[DataRequired()]
    )
    members = FieldList(
        StringField(
            label='members',
            validators=[
            DataRequired(),
            UUID()
        ]),
        min_entries=1
    )
    questionRecords = FieldList(
        FormField(PostQuestionRecordForm),
        min_entries=1
    )
    
# class DeleteQuizRecordForm(FlaskForm):
#     quizRecordId = StringField(
#         label='quizRecordId',
#         validators=[
#             DataRequired(),
#             UUID()
#         ]
#     )

   
    