import uuid
from QuizBankBackend.db import db
from QuizBankBackend.quiz.form import *
from QuizBankBackend.utility import setResponse
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
QUIZTYPE = ['casual', 'single']

class AllQuizResource(Resource):
    @jwt_required()
    def get(self):
        quizType = request.args.get('quizType')
        userId = get_jwt_identity()
        quizFilter = {'type': quizType, 'members': {"$in" : [userId]} }
        quiz = list(db.quizs.find(quizFilter))
        try:
            batch = int(request.args.get('batch'))
        except ValueError:
            response = setResponse(400, 'Failed to get all quizRecord.')
            return response
        
        
        if quiz is None:
            response = setResponse(
            404, 'quiz not found.')
            return response
        if len(quiz)>30:
            quiz = quiz[batch*30: (batch+1)*30]

        response = setResponse(
            200,
            'Get all quiz successfully.',
            'quizList',
            quiz
        )
        return response
        
        
class QuizResource(Resource):
    def get(self): 
        quizId = request.args.get('quizId')
        quizFilter = {'_id': quizId}
        quiz = db.quizs.find_one(quizFilter)
        
        if quizId is None:
            response = setResponse(400, 'Failed to get quizRecord.')
            return response
        if quiz is None:
            response = setResponse(404, 'Quiz  not found.')
            return response

        response = setResponse(
            200,
            'Get quiz successfully.',
            'quiz',
            quiz
        )
        return response

        
    @jwt_required()
    def post(self):
        formJson = request.get_json()
        form = PostQuizForm.from_json(formJson)

        if form.validate():
            quizId = str(uuid.uuid4())
            formJson['_id'] = quizId
            userId = get_jwt_identity()
            for questions in formJson['questions']:
                questionId = str(uuid.uuid4())
                questions['_id'] = questionId
                questions['provider'] = userId

            db.quizs.insert_one(formJson)
            response = setResponse(200, 'Add quiz successfully', 'quiz', formJson)
            return response
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            response = setResponse(
                400, 'Failed to get quizRecord.')
            return response
        

    @jwt_required()
    def put(self):
        formJson = request.get_json()
        form = PutQuizForm.from_json(formJson)

        if form.validate():
            filter = {'_id': formJson['quizId']}
            del formJson['quizId']
            for question in formJson['questions']:
                question['_id'] = question['questionId']
                del question['questionId']
                
            newQuiz = {'$set': formJson}
            result = db.quizs.update_one(filter, newQuiz)
            if result.matched_count==0:
                response = setResponse(404, 'quiz not found.')
            else:
                response = setResponse(200, 'Update quiz successfully.')
            return response
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
            response = setResponse(400, 'Failed to update quiz.')
            return response

    @jwt_required()
    def delete(self): 
        quizId = request.args.get('quizId')
        
        if quizId is None:
            response = setResponse(
            400, 'Failed to delete quizRecord.')
            return response

        quizFilter = {'_id': quizId}
        result = db.quizs.delete_one(quizFilter)
        if result.deleted_count==0:
            response = setResponse(
            404, 'the quiz that request to delete was not found.')
            return response
        else:
            response = setResponse(
                200, 'delete quiz record successfully.')
            return response