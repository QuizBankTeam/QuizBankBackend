import uuid
from QuizBankBackend.db import db
from QuizBankBackend.quizRecord.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class AllQuizRecordResource(Resource):
    @jwt_required()
    def get(self):
        formJson = request.get_json()
        form = AllQuizRecordForm.from_json(formJson)

        if form.validate():
            userId = get_jwt_identity()
            recordFilter = {'type': formJson['quizRecordType']}
            quizRecords = list(db.quizRecords.find(recordFilter))
            userQuizRecords = []
            for quizRecord in quizRecords:
                members = quizRecord['members']
                for member in members:
                    if member == userId:
                        userQuizRecords.append(quizRecord['_id'])
                        break

            if userQuizRecords is None:
                response = setResponse(404, 'quiz Record not found.')
                return response

            response = setResponse(
                200,
                'Get all quiz records successfully.',
                'quizRecords',
                userQuizRecords
            )
            return response

        response = setResponse(400, 'Failed to get all quiz records.')
        return response
        
class QuizRecordResource(Resource):
    def get(self): 
        formJson = request.get_json()
        form = GetQuizRecordForm.from_json(formJson)
        
        if form.validate():
            quizRecordFilter = {'_id': formJson['quizRecordId']}
            quizRecord = db.quizRecords.find_one(quizRecordFilter)
            questions = []
            questionRecords = []

            if quizRecord is None:
                response = setResponse(404, 'Quiz Record not found.')
                return response
            
            for questionRecordId in quizRecord['questionRecords']:
                questionRecordFilter = {'_id': questionRecordId}
                questionRecords.append(db.questionRecords.find_one(questionRecordFilter))
            print(f'size of questionRecords is{len(questionRecords)}')

            for questionRecord in questionRecords:
                tmpQuestionId = questionRecord['question']
                questionFilter = {'_id': tmpQuestionId}
                questions.append(db.questions.find_one(questionFilter))
            print(f'size of questions is{len(questions)}')

            quizRecord['questions'] = questions
            del quizRecord['questionRecords']
            quizRecord['questionRecords'] = questionRecords

            response = setResponse(
                200,
                'Get quiz record successfully.',
                'quizRecord',
                quizRecord
            )
            return response

        response = setResponse(
            400, 'Failed to get quizRecord.')
        return response

    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostQuizRecordForm.from_json(formJson)
        questionRecordIDs = []
        if form.validate():
            quizRecordId = str(uuid.uuid4())
            formJson['_id'] = quizRecordId
            tmpDate = formJson['startDate']
            print(f'startDate is{tmpDate} startDate type is{type(tmpDate)}')
            for questionRecord in formJson['questionRecords']:
                questionRecord['quizRecord'] = quizRecordId
                questionRecord['_id'] = str(uuid.uuid4())
                questionRecordIDs.append(questionRecord['_id'])

            db.questionRecords.insert_many(formJson['questionRecords'])
            del formJson['questionRecords']
            formJson['questionRecords'] = questionRecordIDs
            db.quizRecords.insert_one(formJson)
            response = setResponse(200, 'Add quizRecord successfully', 'quizRecord', formJson)
            return response
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            response = setResponse(
                400, 'Failed to get quizRecord.')
            return response
        
    @jwt_required()
    def delete(self): 
        formJson = request.get_json()
        form = DeleteQuizRecordForm.from_json(formJson)
        
        if form.validate():
            quizRecordFilter = {'_id': formJson['quizRecordId']}
            questionRecordFilter = {'quizRecord': formJson['quizRecordId']}
            db.quizRecords.delete_one(quizRecordFilter)
            db.questionRecords.delete_many(questionRecordFilter)
            response = setResponse(
                200, 'delete quiz record successfully.')
            return response

        response = setResponse(
            400, 'Failed to delete quizRecord.')
        return response