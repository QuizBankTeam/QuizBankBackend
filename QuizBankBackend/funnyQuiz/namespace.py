from flask_socketio import Namespace, emit
from flask import request
from QuizBankBackend.funnyQuiz.manager import FunnQuizManager


funnyQuizManager = FunnQuizManager()

class FunnyQuizNamespace(Namespace):
    def on_connect(self):
        emit('connected')

    def on_disconnect(self):
        funnyQuizManager.leave_room()
        emit('disconnected')

    def on_join_quiz(self, quizId, userId):
        print(userId + ' join quiz in ' + quizId)
        flag, username = funnyQuizManager.join_room(quizId, userId)
        userCount = len(funnyQuizManager.get_all_users(quizId))
        if flag:
            emit('joinQuiz', (userCount, username), to=quizId)
        else:
            emit('quizNotFound')

    def on_start_quiz(self, quizId, questionId, questionCount):
        print('start quiz in ' + quizId)
        funnyQuizManager.start_quiz(quizId, questionId, questionCount)
        emit('startQuiz', to=quizId)
    
    def on_timeout(self, quizId, userId, qtype, nextQuestionId):
        funnyQuizManager.finish_question(quizId=quizId, userId=userId, qtype=qtype, nextQuestionId=nextQuestionId)
        emit('timeout', userId, to=quizId)

    def on_finish_question(self, quizId, userId, qtype, userAnswer, socre, nextQuestionId):
        isNext = funnyQuizManager.finish_question(quizId, userId, qtype, userAnswer, socre, nextQuestionId)
        emit('finishQuestion', isNext, to=quizId)

    def on_finish_quiz(self, quizId):
        emit('finishQuiz', to=quizId)
        funnyQuizManager.finish_quiz(quizId)

    def on_return_quiz_state(self, quizId):
        quizState = funnyQuizManager.get_quiz_state(quizId)
        emit('returnQuizState', quizState, to=quizId)

    def on_use_ability(self, quizId, attacker, receiver, type):
        abilityIndex = funnyQuizManager.use_ability(quizId, attacker, receiver, type)
        emit('useAbility', (receiver, abilityIndex, type), to=quizId)

    def on_complete_ability(self, quizId, index):
        victim = funnyQuizManager.complete_ability(index)
        emit('completeAbility', victim, to=quizId)

    def on_show_quizs(self, quizId):
        quizs = funnyQuizManager.get_all_quizs()
        emit('showQuizs', quizs)