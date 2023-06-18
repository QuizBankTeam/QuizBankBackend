import os
import wtforms_json
from flask import Flask
from flask_wtf.csrf import CSRFProtect, generate_csrf 
from flask_restful import Api, Resource
from QuizBankBackend.utility import setResponse


app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)
api = Api(app)
wtforms_json.init()

class CSRFToken(Resource):
    def get(self):
        response = setResponse(200, 'Hello world!')
        response.set_cookie('CSRF-TOKEN', generate_csrf())
        return response


api.add_resource(CSRFToken, '/')


import QuizBankBackend.db
from QuizBankBackend.question import router
from QuizBankBackend.questionSet import router
from QuizBankBackend.questionBank import router
