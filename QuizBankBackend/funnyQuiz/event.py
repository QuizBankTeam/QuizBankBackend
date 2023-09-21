from QuizBankBackend import socketio
from QuizBankBackend.funnyQuiz.namespace import FunnyQuizNamespace


socketio.on_namespace(FunnyQuizNamespace('/funnyQuiz'))