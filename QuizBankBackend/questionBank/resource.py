import uuid
from QuizBankBackend.db import db
from QuizBankBackend.questionBank.form import *
from QuizBankBackend.utility import setResponse
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
        formJson = request.get_json()
        form = PostQuestionBankForm.from_json(formJson)

        if form.validate():
            formJson['_id'] = str(uuid.uuid4())
            formJson['creator'] = get_jwt_identity()

            originateFrom = db.users.find_one({'_id': formJson['originateFrom']})
            members = formJson['members']

            if originateFrom is None:
                response = setResponse(400, 'Original user does not existed.')
                return response

            for member in members:
                user = db.users.find_one({'_id': member})
                if user is None:
                    response = setResponse(400, 'Member ' + member + ' does not existed.')
                    return response

            db.questionBanks.insert_one(formJson)

            response = setResponse(
                201,
               'Create a question bank successfully.',
               'questionBank',
               formJson
            )
            return response

        response = setResponse(400, 'Failed to create a question bank.')
        return response

    @jwt_required()
    def put(self):
        formJson = request.get_json()
        form = PutQuestionBankForm.from_json(formJson)

        if form.validate():
            filter = {'_id': formJson['questionBankId']}
            questionBank = formJson.copy()
            del questionBank['questionBankId']
            members = formJson['members']

            for member in members:
                user = db.users.find_one({'_id': member})
                if user is None:
                    response = setResponse(400, 'Member ' + member + ' does not existed.')
                    return response

            db.questionBanks.update_one(filter, {'$set': questionBank})
            questionBank = db.questionBanks.find_one(filter)
            response = setResponse(
                200,
                'Update question bank info successfully.',
                'questionBank',
                questionBank
            )
            return response

        response = setResponse(400, 'Failed to update question bank info.')
        return response

    @jwt_required()
    def delete(self, questionBankId):
        db.questionBanks.delete_one({'_id': questionBankId})
        db.questions.delete_many({'questionBank': questionBankId})
        db.questionSets.delete_many({'questionBank': questionBankId})

        response = setResponse(200, 'Delete question bank successfully.')
        return response

