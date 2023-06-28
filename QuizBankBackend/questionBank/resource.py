import uuid
from QuizBankBackend.db import db
from QuizBankBackend.questionBank.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class AllQuestionBankResource(Resource):
    @jwt_required()
    def get(self):
        formJson = request.get_json()
        form = GetAllQuestionBanksForm.from_json(formJson)
        
        if form.validate():
            userId = get_jwt_identity()
            banks = db.questionBanks.find({'creator': userId})
            if banks is None:
                response = setResponse(404, 'Question banks not found.')
                return response

            response = setResponse(
                200,
                'Get all question banks successfully.',
                'questionBanks',
                list(banks)
            )
            return response

        response = setResponse(400, 'Failed to get all question banks.')
        return response

class QuestionBankResource(Resource):
    def get(self):
        formJson = request.get_json()
        form = GetQuestionBankForm.from_json(formJson)

        if form.validate():
            bankFilter = {'_id': formJson['questionBankId']}
            questionFilter = {'questionBank': bankFilter['_id']}
            questionBank = db.questionBanks.find_one(bankFilter)
            questionSets = list(db.questionSets.find(questionFilter))
            questions = list(db.questions.find(questionFilter))

            questionBank['questionSets'] = questionSets
            questionBank['questions'] = questions
            if questionBank is None:
                response = setResponse(404, 'Question bank not found.')
                return response

            response = setResponse(
                200,
                'Get quesitons from question bank successfully.',
                'questionBank',
                questionBank
            )
            return response

        response = setResponse(
            400, 'Failed to get questions from question bank.')
        return response

    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostQuestionBankForm.from_json(formJson)

        if form.validate():
            formJson['_id'] = str(uuid.uuid4())
            formJson['creator'] = get_jwt_identity()
            db.questionBanks.insert_one(formJson)
            response = setResponse(201, 'Create a question bank successfully.')
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
            # print(questionBank)
            db.questionBank.update_one(filter, {'$set': questionBank})

            response = setResponse(
                200, 'Update question bank info successfully.')
            return response

        response = setResponse(400, 'Failed to update question bank info.')
        return response

    @jwt_required()
    def delete(self):
        formJson = request.get_json()
        form = DeleteQuestionBankForm.from_json(formJson)

        if form.validate():
            filter = {'_id': formJson['questionBankId']}
            db.questions.delete_many(filter)
            db.questionSets.delete_many(filter)

            response = setResponse(200, 'Delete question bank successfully.')
            return response

        response = setResponse(400, 'Failed to delete question bank.')
        return response
