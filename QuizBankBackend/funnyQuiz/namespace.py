from flask_socketio import Namespace, emit
from QuizBankBackend.funnyQuiz.manager import FunnQuizManager


funnyQuizManager = FunnQuizManager()

class FunnyQuizNamespace(Namespace):
    def on_connect(self):
        emit('connected')

    def on_disconnect(self):
        emit('disconnected')

    def on_join_quiz(self, quizId, userId):
        print(userId + ' join quiz in ' + quizId)
        funnyQuizManager.join_room(quizId, userId)
        emit('joinQuiz', to=quizId)

    def on_start_quiz(self, quizId, questionId, questionCount):
        print('start quiz in ' + quizId)
        funnyQuizManager.start_quiz(quizId, questionId, questionCount)
        emit('startQuiz', to=quizId)

    def on_timeout(self, quizId, nextQuestionId):
        funnyQuizManager.finish_question(quizId, nextQuestionId)
        emit('timeout', to=quizId)

    def on_finish_question(self, quizId, nextQuestionId):
        funnyQuizManager.finish_question(quizId, nextQuestionId)
        emit('finishQuestion', to=quizId)

    def on_finish_quiz(self, quizId):
        funnyQuizManager.remove_room(quizId)
        emit('finishQuiz', to=quizId)