from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField
from wtforms.validators import DataRequired 
from QuizBankBackend.question.form import PostQuestionForm

class GetQuestioSetForm(FlaskForm):
    class Meta:
        csrf = False

    questionSetId = StringField(label='questionSetId', validators=[DataRequired()])

class PostQuestionSetForm(FlaskForm):
    description = StringField(label='description', validators=[DataRequired()])
    image = FieldList(StringField(validators=[DataRequired()]))
    questionBank = StringField(label='questionBank', validators=[DataRequired()]) 
    questions = FieldList(FormField(PostQuestionForm))
    provider = StringField(label='provider', validators=[DataRequired()])
    createdDate = StringField(label='createdDate', validators=[DataRequired()])
    orginateFrom = StringField(label='orginateFrom', validators=[DataRequired()])

class PutQuestionSetForm(FlaskForm):
    questionSetId = StringField(label='questionSetId', validators=[DataRequired()])
    description = StringField(label='description', validators=[DataRequired()])
    image = FieldList(StringField(validators=[DataRequired()]))
    questionBank = StringField(label='questionBank', validators=[DataRequired()]) 
    questions = FieldList(FormField(PostQuestionForm))
    provider = StringField(label='provider', validators=[DataRequired()])
    createdDate = StringField(label='createdDate', validators=[DataRequired()])
    orginateFrom = StringField(label='orginateFrom', validators=[DataRequired()])

class DeleteQuestionSetForm(FlaskForm):
    questionSetId = StringField(label='questionSetId', validators=[DataRequired()])
