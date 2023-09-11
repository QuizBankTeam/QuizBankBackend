import uuid
from QuizBankBackend.db import db
from QuizBankBackend.user.form import *
from QuizBankBackend.utility import setResponse, formFieldError
from QuizBankBackend.user.callback import *
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    unset_access_cookies,
    set_access_cookies,
    set_refresh_cookies,
    jwt_required,
    get_jwt_identity
)


class UserProfileResource(Resource):
    def get(self, username):
        user = db.users.find_one({'username': username})

        if user is None:
            response = setResponse(404, 'User not found.')
            return response

        del user['password']
        response = setResponse(200, 'Get user successfully.', 'user', user)
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

        return formFieldError(form)

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

            del user['password']
            response = setResponse(200, 'Login successfully.', 'user', user)
            set_access_cookies(response, create_access_token(identity=user['_id']))
            set_refresh_cookies(response, create_refresh_token(identity=user['_id']))
            return response

        return formFieldError(form)

class LogoutResource(Resource):
    def post(self):
        response = setResponse(200, 'Logout successfully.')
        unset_access_cookies(response)
        return response

class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        response = setResponse(200, 'Refresh token successfully.')
        set_access_cookies(response, create_access_token(identity=identity))
        return response

class ResetPasswordResource(Resource):
    @jwt_required()
    def patch(self):
        formJson = request.get_json()
        form = ResetPasswordForm.from_json(formJson)

        if form.validate():
            userId = get_jwt_identity()
            user = db.users.find_one({'_id': userId})

            if user is None:
                response = setResponse(404, 'User not found.')
                return response
            elif user['password'] != formJson['password']:
                response = setResponse(401, 'Wrong password.')
                return response
            elif user['password'] == formJson['newPassword']:
                response = setResponse(409, 'New password is the same as the old one.')
                return response
            elif formJson['newPassword'] != formJson['confirmNewPassword']:
                response = setResponse(409, 'Confirm password is not the same as the new one.')
                return response

            db.users.update_one(
                {'_id': userId},
                {'$set': {'password': formJson['newPassword']}}
            )

            response = setResponse(200, 'Reset password successfully.')
            return response

        return formFieldError(form)

class ForgotPasswordResource(Resource):
    def post(self):
        formJson = request.get_json()
        form = ForgotPasswordForm.from_json(formJson)

        if form.validate():
            user = db.users.find_one({'email': formJson['email']})

            if user is None:
                response = setResponse(404, 'User not found.')
                return response

            sendEmail(user)

            response = setResponse(200, 'Forgot password successfully.')
            return response

        return formFieldError(form)

class VerifyTokenResource(Resource):
    def get(self, token):
        user = verifyUserJWSToken(token)
        if user is None:
            response = setResponse(401, 'Invalid token. Please try again.')
            return response

        response = setResponse(200, 'Reset token successfully.')
        return response
