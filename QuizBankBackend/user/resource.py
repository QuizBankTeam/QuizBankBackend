import uuid
from QuizBankBackend.db import db
from QuizBankBackend.user.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token


class UserProfileResource(Resource):
    def get(self):
        formJson = request.get_json()
        form = GetUserForm.from_json(formJson)

        print(form.errors)
        if form.validate():
            user = db.users.find_one({'_id': formJson['userId']})

            if user is None:
                response = setResponse(404, 'User not found.')
                return response
            else:
                del user['password']

            response = setResponse(200, 'Get user successfully.', 'user', user)
            return response

        response = setResponse(400, 'Failed to get user profile.')
        return response

class RegisterResource(Resource):
    def post(self):
        formJson = request.get_json()
        form = RegisterForm.from_json(formJson)

        if form.validate():
            status = 201
            msg = 'Register successfully.'
            if db.users.find_one({'username': formJson['username']}):
                status = 409
                msg = 'Username already exists.'
            elif db.users.find_one({'email': formJson['email']}):
                status = 409
                msg = 'Email already exists.'
            elif db.users.find_one({'password': formJson['password']}):
                status = 409
                msg = 'Password already exists.'
            else:
                userId = str(uuid.uuid4())
                formJson['_id'] = userId
                formJson['preference'] = []
                formJson['roles'] = []
                formJson['introduction'] = ''
                formJson['avatar'] = ''
                formJson['group'] = []
                formJson['status'] = False
                formJson['questionRecords'] = []
                db.users.insert_one(formJson)

            response = setResponse(status, msg)
            return response

class LoginResource(Resource):
    def post(self):
        formJson = request.get_json()
        form = LoginForm.from_json(formJson)

        if form.validate():
            user = db.users.find_one({'username': formJson['username']})

            if user is None:
                response = setResponse(404, 'User not found.')
                return response
            elif user['password'] != formJson['password']:
                response = setResponse(401, 'Wrong password.')
                return response
            else:
                del user['password']

            response = setResponse(200, 'Login successfully.', 'user', user)
            response.set_cookie("access_token", create_access_token(identity=user['_id']))
            return response

        response = setResponse(400, 'Failed to login.')
        return response

class LogoutResource(Resource):
    def post(self):
        response = setResponse(200, 'Logout successfully.')
        response.set_cookie("access_token", '', expires=0)
        return response
