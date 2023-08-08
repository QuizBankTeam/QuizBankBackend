import uuid
from QuizBankBackend.db import db
from QuizBankBackend.question.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class QuestionResource(Resource):
    def get(self, questionId):
        question = db.questions.find_one({'_id': questionId})

        if question is None:
            response = setResponse(404, 'Question not found.')
            return response
        else:
            response = setResponse(
                200, 'Get question successfully.', 'question', question)
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
            del formJson['questionId']
            newQuesiton = {'$set': formJson}
            db.questions.update_one(filter, newQuesiton)
            response = setResponse(200, 'Update question successfully.')
            return response

        response = setResponse(400, 'Failed to update question.')
        return response

    @jwt_required()
    def delete(self, questionId):
        db.questions.delete_one({'_id': questionId})
        response = setResponse(200, 'Delete question successfully.')
        return response

class AnswerResource(Resource):
    @jwt_required()
    def patch(self):
        formJson = request.get_json()
        form = PatchAnswerForm.from_json(formJson)

        if form.validate():
            if formJson['questionSetId'] is None:
                filter = {'_id': formJson['questionId']}
                answer = {'$set': {
                    'answerOptions': formJson['answerOptions'],
                    'answerDescription': formJson['answerDescription']
                }}
                db.questions.update_one(filter, answer)
            else:
                filter = {
                    '_id': formJson['questionSetId'],
                    'questions._id': formJson['questionId']
                }
                answer = {'$set': {
                    'questions.$.answerOptions': formJson['answerOptions'],
                    'questions.$.answerDescription': formJson['answerDescription']
                }}
                db.questionSets.update_one(filter, answer)
            response = setResponse(200, 'Update answer successfully.')
            return response

        response = setResponse(400, 'Failed to update answer.')
        return response
    
class TagResource(Resource):
    @jwt_required()
    def patch(self):
        formJson = request.get_json()
        form = PatchTagForm.from_json(formJson)

        if form.validate():
            if formJson['questionSetId'] is None:
                filter = {'_id': formJson['questionId']}
                tag = {'$set': {'tag': formJson['tag']}}
                db.questions.update_one(filter, tag)
            else:
                filter = {
                    '_id': formJson['questionSetId'],
                    'questions._id': formJson['questionId']
                }
                tag = {'$set': {
                    'questions.$.tag': formJson['tag']
                }}
                db.questionSets.update_one(filter, tag)
            response = setResponse(200, 'Update tag successfully.')
            return response

        response = setResponse(400, 'Failed to update tag.')
        return response