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
        userCount = len(funnyQuizManager.get_all_users(quizId))
        emit('joinQuiz', userCount, to=quizId)

    def on_start_quiz(self, quizId, questionId, questionCount):
        print('start quiz in ' + quizId)
        funnyQuizManager.start_quiz(quizId, questionId, questionCount)
        emit('startQuiz', to=quizId)
    
    def on_timeout(self, quizId, userId, nextQuestionId):
        funnyQuizManager.finish_question(quizId=quizId, userId=userId, nextQuestionId=nextQuestionId)
        emit('timeout', userId, to=quizId)

    def on_finish_question(self, quizId, userId, userAnswer, socre, nextQuestionId):
        isNext = funnyQuizManager.finish_question(quizId, userId, userAnswer, socre, nextQuestionId)
        emit('finishQuestion', isNext, to=quizId)

    def on_finish_quiz(self, quizId):
        funnyQuizManager.finish_quiz(quizId)
        emit('finishQuiz', to=quizId)

    def on_return_quiz_state(self, quizId):
        quizState = funnyQuizManager.get_quiz_state(quizId)
        emit('returnQuizState', quizState, to=quizId)