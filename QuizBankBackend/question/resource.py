import uuid
from QuizBankBackend.db import db
from QuizBankBackend.question.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class QuestionResource(Resource):
    def get(self):
        formJson = request.get_json()
        form = GetQuestionForm.from_json(formJson)

        if form.validate():
            question = db.questions.find_one(formJson['questionId'])

            if question is None:
                response = setResponse(404, 'Question not found.')
                return response
            else:
                response = setResponse(
                    200, 'Get question successfully.', 'question', question)
                return response

        response = setResponse(400, 'Failed to get question.')
        return response

    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostQuestionForm.from_json(formJson)

        if form.validate():
            questionId = str(uuid.uuid4())
            formJson['_id'] = questionId
            formJson['provider'] = get_jwt_identity()
            db.questions.insert_one(formJson)
            response = setResponse(201, 'Add question successfully!')
            return response

        response = setResponse(400, 'Failed to add question.')
        return response

    @jwt_required()
    def put(self):
        formJson = request.get_json()
        form = PutQuestionForm.from_json(formJson)

        if form.validate():
            filter = {'_id': formJson['questionId']}
            newQuesiton = {'$set': formJson}
            db.questions.update_one(filter, newQuesiton)
            response = setResponse(200, 'Update question successfully.')
            return response

        response = setResponse(400, 'Failed to update question.')
        return response

    @jwt_required()
    def delete(self):
        formJson = request.get_json()
        form = DeleteQuestionForm.from_json(formJson)

        if form.validate():
            db.questions.delete_one({'_id': formJson['questionId']})
            response = setResponse(200, 'Delete question successfully.')
            return response

        response = setResponse(400, 'Failed to delete question.')
        return response
