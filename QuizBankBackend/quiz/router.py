from QuizBankBackend import api
from QuizBankBackend.quiz.resource import *

api.add_resource(QuizResource, '/quiz')
api.add_resource(AllQuizResource, '/allQuizs')