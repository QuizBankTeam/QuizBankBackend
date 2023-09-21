from flask_socketio import join_room, leave_room, close_room
from threading import Timer
from QuizBankBackend.db import db

class FunnQuizManager:
    def __init__(self):
        self.rooms = {}  # 用于存储房间的字典，键是房间ID，值是房间对象

    def create_room(self, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = {
                'members': set(),
                'question': {
                    'current_id': None,
                    'current_index': 0,
                    'received': 0,
                },
                'count': 0
            }

    def join_room(self, room_id, user_id):
        if room_id in self.rooms:
            self.rooms[room_id]['users'].add(user_id)

        join_room(room_id)

    def leave_room(self, room_id, user_id):
        if room_id in self.rooms:
            self.rooms[room_id]['users'].discard(user_id)

        leave_room(room_id)

    def get_room_users(self, room_id):
        if room_id in self.rooms:
            return list(self.rooms[room_id]['users'])

        return []

    def get_all_rooms(self):
        return list(self.rooms.keys())

    def remove_room(self, room_id):
        if room_id in self.rooms:
            if self.rooms['count'] == self.rooms['question']['current_index']:
                close_room(room_id)
                del self.rooms[room_id]

    def start_quiz(self, quizId, questionId, questionCount):
        if quizId in self.rooms:
            # quiz = db.quizs.find_one({'_id': quizId})
            question = self.rooms[quizId]['question']
            question['current_id'] = questionId
            self.rooms[quizId]['count'] = questionCount

    def finish_question(self, quizId, nextQuestionId=None):
        if quizId in self.rooms:
            if question['received'] == len(self.rooms[quizId]['users']):
                question = self.rooms[quizId]['question']
                question['current_id'] = nextQuestionId
                question['received'] = 0
                question['current_index'] += 1
                return True

            question['received'] += 1
            return False