from QuizBankBackend import api
from QuizBankBackend.questionSet.resource import *


api.add_resource(QuestionSetResource, '/questionSet', '/questionSet/<string:questionSetId>')
api.add_resource(MoveQuestionSetResource, '/questionSet/move')