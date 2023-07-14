from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField, FormField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, UUID, Optional

QUIZ_TYPE = ['single', 'casual']
CORRECT = ['true', 'false']
QUIZRECORDTYPE = ['casual', 'single']

class PostQuestionRecordForm(FlaskForm):
    user = StringField(
        label='user',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    userAnswer = StringField(
        label='userAnswer',
        validators=[DataRequired()]
    )
    correct = SelectField(
        label='correct',
        choices=CORRECT,
        validators=[DataRequired()]
    )
    date = DateField(
        label='date',
        validators=[DataRequired()]
    )
    question = StringField(
        label='question',
        validators=[
            DataRequired(),
            UUID()
        ]
    )

class AllQuizRecordForm(FlaskForm):
    class Meta:
        csrf = False
        
    quizRecordType = SelectField(
        label='quizRecordType',
        choices=QUIZRECORDTYPE,
        validators=[
            DataRequired()
        ]
    )

class GetQuizRecordForm(FlaskForm):
    class Meta:
        csrf = False

    quizRecordId = StringField(
        label='quizRecordId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )


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
    date = DateField(
        label='date',
        validators=[DataRequired()]
    )
    type = SelectField(
        label='type',
        choices=QUIZ_TYPE
    )
    totalScore = IntegerField(
        label='date',
        validators=[DataRequired()]
    )
    durningTime = IntegerField(
        label='date',
        validators=[DataRequired()]
    )
    startDate = DateTimeField(
            label='startDate',
            validators=[DataRequired()]
        )
    endDate = DateTimeField(
        label='endDate',
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
    
class DeleteQuizRecordForm(FlaskForm):
    quizRecordId = StringField(
        label='quizRecordId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )

   
    