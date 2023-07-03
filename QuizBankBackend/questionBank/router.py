from QuizBankBackend import api
from QuizBankBackend.questionBank.resource import *


api.add_resource(QuestionBankResource, '/questionBank', '/questionBank/<string:questionBankId>')
api.add_resource(AllQuestionBankResource, '/questionBanks/<string:bankType>')
