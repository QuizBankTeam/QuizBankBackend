from QuizBankBackend import api
from QuizBankBackend.question.resource import *


api.add_resource(QuestionResource, '/question', '/question/<string:questionId>')
api.add_resource(AnswerResource, '/question/answer')
api.add_resource(TagResource, '/question/tag')
api.add_resource(MoveQuestionResource, '/question/move')