import uuid
from QuizBankBackend.db import db
from QuizBankBackend.questionSet.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class QuestionSetResource(Resource):
    def get(self, questionSetId):
        questionSet = db.questionSets.find_one({'_id': questionSetId})

        if questionSet is None:
            response = setResponse(404, 'Question set not found.')
            return response
        else:
            response = setResponse(
                200, 'Get question set successfully.', 'questionSet', questionSet)
            return response


    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostQuestionSetForm.from_json(formJson)

        if form.validate():
            questionSetId = str(uuid.uuid4())
            formJson['_id'] = questionSetId
            formJson['provider'] = get_jwt_identity()
            for question in formJson['questions']:
                question['_id'] = str(uuid.uuid4())
                question['provider'] = get_jwt_identity()
            db.questionSets.insert_one(formJson)
            response = setResponse(201, 'Add question set successfully!')
            return response

        response = setResponse(400, 'Failed to add question set.')
        return response

    @jwt_required()
    def put(self):
        formJson = request.get_json()
        form = PutQuestionSetForm.from_json(formJson)

        print(form.errors)
        if form.validate():
            filter = {'_id': formJson['questionSetId']}
            newQuestionSet = {'$set': formJson}
            db.questionSets.update_one(filter, newQuestionSet)
            response = setResponse(200, 'Update question set successfully.')
            return response

        response = setResponse(400, 'Failed to update question set.')
        return response

    @jwt_required()
    def delete(self, questionSetId):

        db.questionSets.delete_one({'_id': questionSetId})
        response = setResponse(200, 'Delete question set successfully.')
        return response