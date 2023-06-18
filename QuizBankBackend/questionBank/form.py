from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, DateField, SelectField
from wtforms.validators import DataRequired, UUID

class GetQuestionBankForm(FlaskForm):
    class Meta:
        csrf = False

    questionBankId = StringField(
                label='questionBankId',
                validators=[
                    DataRequired(),
                    UUID()
                ]
            )

QUESTION_BANK_TYPE = ['multi', 'single', 'public']

class PostQuestionBankForm(FlaskForm):
    title = StringField(
                label='title',
                validators=[DataRequired()]
            )
    questionBankType = SelectField(
                label='questionBankType',
                choices=QUESTION_BANK_TYPE
            )
    createdDate = DateField(
                label='createdDate',
                validators=[DataRequired()]
            )
    members = FieldList(
                StringField(validators=[
                    DataRequired(),
                    # UUID()
                ]),
                min_entries=1
            )
    creator = StringField(
                label='creator',
                validators=[DataRequired()]
            )

class PutQuestionBankForm(PostQuestionBankForm):
    questionBankId = StringField(
                label='questionBankId',
                validators=[
                    DataRequired(),
                    UUID()
                ]
            )

class DeleteQuestionBankForm(GetQuestionBankForm):
    class Meta:
        csrf = True
