from QuizBankBackend import api
from QuizBankBackend.quizRecord.resource import *

api.add_resource(QuizRecordResource, '/quizRecord')
api.add_resource(AllQuizRecordResource, '/allQuizRecords')