import uuid
from QuizBankBackend.db import db
from QuizBankBackend.questionBank.form import *
from QuizBankBackend.utility import (
    setResponse,
    formFieldError,
    requestToForm,
    formToJson
)
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class AllQuestionBankResource(Resource):
    @jwt_required()
    def get(self, bankType):
        userId = get_jwt_identity()
        banks = db.questionBanks.find({
            'creator': userId,
            'questionBankType': bankType
        })

        response = setResponse(
            200,
            'Get all question banks successfully.',
            'questionBanks',
            list(banks)
        )
        return response

class QuestionBankResource(Resource):
    def get(self, questionBankId):

        bankFilter = {'_id': questionBankId}
        questionFilter = {'questionBank': questionBankId}
        questionBank = db.questionBanks.find_one(bankFilter)

        if questionBank is None:
            response = setResponse(404, 'Question bank not found.')
            return response

        questionSets = list(db.questionSets.find(questionFilter))
        questions = list(db.questions.find(questionFilter))

        questionBank['questionSets'] = questionSets
        questionBank['questions'] = questions

        response = setResponse(
            200,
            'Get quesitons from question bank successfully.',
            'questionBank',
            questionBank
        )
        return response

    @jwt_required()
    def post(self):
        form = requestToForm(request, PostQuestionBankForm)
        formJson = formToJson(form)

        if form.validate():
            formJson['_id'] = str(uuid.uuid4())
            formJson['creator'] = get_jwt_identity()
            formJson['createdDate'] = formJson['createdDate'].strftime('%Y-%m-%d')

            originateFrom = db.users.find_one({'_id': formJson['originateFrom']})
            members = formJson['members']

            if originateFrom is None:
                response = setResponse(400, 'Original user does not existed.')
                return response

            users = db.users.find({'_id': {'$in': members}})

            missingMembers = set(members) - set(users.distinct('_id'))
            if len(missingMembers) != 0:
                response = setResponse(400, f'{missingMembers} does not existed.')
                return response

            db.questionBanks.insert_one(formJson)

            response = setResponse(
                201,
               'Create a question bank successfully.',
               'questionBank',
               formJson
            )
            return response

        return formFieldError(form)

    @jwt_required()
    def put(self):
        form = requestToForm(request, PutQuestionBankForm)
        formJson = formToJson(form)

        if form.validate():
            filter = {'_id': formJson['questionBankId']}
            questionBank = formJson.copy()
            del questionBank['questionBankId']
            members = formJson['members']

            missingMembers = set(members) - set(users.distinct('_id'))
            if len(missingMembers) != 0:
                response = setResponse(400, f'{missingMembers} does not existed.')
                return response

            result = db.questionBanks.update_one(filter, {'$set': questionBank})

            if result.modified_count == 0:
                response = setResponse(404, 'Question bank not found or nothing changed.')
                return response

            questionBank = db.questionBanks.find_one(filter)
            response = setResponse(
                200,
                'Update question bank info successfully.',
                'questionBank',
                questionBank
            )
            return response

        return formFieldError(form)

    @jwt_required()
    def delete(self, questionBankId):
        result = db.questionBanks.delete_one({'_id': questionBankId})

        if result.deleted_count == 0:
            response = setResponse(404, 'Question bank not found.')
            return response

        db.questions.delete_many({'questionBank': questionBankId})
        db.questionSets.delete_many({'questionBank': questionBankId})

        response = setResponse(200, 'Delete question bank successfully.')
        return response
