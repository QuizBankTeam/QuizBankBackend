from flask_socketio import join_room, close_room
from QuizBankBackend.db import db

class FunnQuizManager:
    def __init__(self):
        self.rooms = {}

    def __create_quiz(self, room_id):
        if room_id not in self.rooms:
            quiz = db.quizs.find_one({'_id': room_id})
            self.rooms[room_id] = {
                'members': set(),
                'userStates':{},
                'question': {
                    'current_id': None,
                    'current_index': 0,
                    'received': 0,
                },
                'count': 0,
                'answers': {},
            }
            for question in quiz['questions']:
                self.rooms[room_id]['answers'][question['_id']] = question['answerOptions']
    
    def get_all_users(self, quizId):
        return list(self.rooms[quizId]['members'])

    def join_room(self, room_id, user_id):
        if room_id not in self.rooms:
            self.__create_quiz(room_id)

        self.rooms[room_id]['members'].add(user_id)
        self.rooms[room_id]['userStates'][user_id] = {
            'score': 0,
            'records': {},
        }
        join_room(room_id)

    def start_quiz(self, quizId, questionId, questionCount):
        if quizId in self.rooms:
            question = self.rooms[quizId]['question']
            question['current_id'] = questionId
            self.rooms[quizId]['count'] = questionCount

    def finish_quiz(self, room_id):
        if room_id in self.rooms:
            if self.rooms[room_id]['count'] == self.rooms['question']['current_index']:
                close_room(room_id)
                del self.rooms[room_id]

    def finish_question(self, quizId, userId, userAnswer=None, score=0, nextQuestionId=None):
        if quizId in self.rooms:
            users = self.rooms[quizId]['userStates']
            question = self.rooms[quizId]['question']
            questionId = question['current_id']

            users[userId]['records'][questionId] = userAnswer
            users[userId]['score'] += score

            if question['received'] == len(self.rooms[quizId]['members']):
                question['current_id'] = nextQuestionId
                question['received'] = 0
                question['current_index'] += 1
                return True

            question['received'] += 1
            return False

    def get_quiz_state(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        return None