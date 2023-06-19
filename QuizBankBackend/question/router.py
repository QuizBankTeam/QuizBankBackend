from QuizBankBackend import api
from QuizBankBackend.question.resource import *

api.add_resource(QuestionResource, '/question')