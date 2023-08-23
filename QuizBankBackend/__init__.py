import os
import json
import logging
import wtforms_json
from flask import Flask, Blueprint
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from QuizBankBackend.utility import setResponse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_app():
    global app, mail, csrf, jwt, api, config, limiter
    app = Flask(__name__, instance_relative_config=True)

    config = open('QuizBankBackend/setting.json')
    config = json.load(config)

    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri=config['MongodbUri'],
        strategy="fixed-window"
    )

    credentialPath = config['OCRCredentialPath']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('HOME') + credentialPath
    os.environ['GCLOUD_PROJECT'] = config['GCPProjectId']

    app.config.from_pyfile('config.py')

    mail = Mail(app)
    csrf = CSRFProtect(app)
    jwt = JWTManager(app)
    api = Api(app)
    wtforms_json.init()

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    class CSRFToken(Resource):
        def get(self):
            response = setResponse(200, 'Hello world!')
            # response.set_cookie('CSRF-TOKEN', generate_csrf(), httponly=True, secure=True)
            response.set_cookie('CSRF-TOKEN', generate_csrf(), httponly=True)
            return response


    api.add_resource(CSRFToken, '/')

    from QuizBankBackend import db
    from QuizBankBackend.question import router
    from QuizBankBackend.questionSet import router
    from QuizBankBackend.questionBank import router
    from QuizBankBackend.user import router
    from QuizBankBackend.quiz import router
    from QuizBankBackend.quizRecord import router
    from QuizBankBackend.scanner import router

    return app
