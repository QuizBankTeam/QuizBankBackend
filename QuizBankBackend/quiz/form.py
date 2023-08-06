from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SelectField, DateField, FormField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, UUID, Optional

QUIZ_STATUS = ['draft', 'ready', 'doing']
QUIZ_TYPE = ['single', 'casual']
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

class PutQuestionForm(FlaskForm):
    questionId = StringField(
        label='questionId',
        validators=[DataRequired(), UUID()]
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
        validators=[DataRequired(), UUID()]
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



class PostQuizForm(FlaskForm):
    title = StringField(
        label='title',
        validators=[DataRequired()]
    )
    type = SelectField(
        label='type',
        choices=QUIZ_TYPE,
        validators=[DataRequired()]
    )
    status = StringField(
        label='status',
        validators=[DataRequired()]
    )
    duringTime = IntegerField(
        label='duringTime',
    )
    casualDuringTime = FieldList(
        IntegerField(
            label='casualDuringTime'
        )
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
    questions = FieldList(
        FormField(PostQuestionForm)
    )
    
    
class PutQuizForm(FlaskForm):
    quizId = StringField(
        label='quizId',
        validators=[
            DataRequired(),
            UUID()
        ]
    )
    title = StringField(
        label='title',
        validators=[DataRequired()]
    )
    status = SelectField(
        label='status',
        choices=QUIZ_STATUS,
        validators=[DataRequired()]
    )
    duringTime = IntegerField(
        label='duringTime',
        validators=[DataRequired()]
    )
    casualDuringTime = FieldList(
        IntegerField(
            label='casualDuringTime',
        )
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
    questions = FieldList(
        FormField(PutQuestionForm)
    )


