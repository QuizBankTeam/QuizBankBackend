from QuizBankBackend import api
from QuizBankBackend.questionBank.resource import *

api.add_resource(QuestionBankResource, '/questionBank')
api.add_resource(AllQuestionBankResource, '/questionBanks')
