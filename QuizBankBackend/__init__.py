import os
import json
import wtforms_json
from datetime import timedelta
from flask import Flask
from flask_wtf.csrf import CSRFProtect, generate_csrf 
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from QuizBankBackend.utility import setResponse
from google.cloud import vision


app = Flask(__name__, instance_relative_config=True)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['JWT_SECRET_KEY'] = os.urandom(24)
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

csrf = CSRFProtect(app)
jwt = JWTManager(app)
api = Api(app)
wtforms_json.init()

config = open('QuizBankBackend/setting.json')
config = json.load(config)
credentialPath = config['OCRCredentialPath']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentialPath

class CSRFToken(Resource):
    def get(self):
        response = setResponse(200, 'Hello world!')
        response.set_cookie('CSRF-TOKEN', generate_csrf(), httponly=True, secure=True)
        return response


api.add_resource(CSRFToken, '/')


from QuizBankBackend import db
from QuizBankBackend.question import router
from QuizBankBackend.questionSet import router
from QuizBankBackend.questionBank import router
from QuizBankBackend.user import router
from QuizBankBackend.scanner import router
