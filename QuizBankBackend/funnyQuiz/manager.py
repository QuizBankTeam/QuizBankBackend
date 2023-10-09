from flask_socketio import join_room, close_room
from QuizBankBackend.db import db


class AbilityManager:
    def __init__(self):
        self.type = ['stall']
        self.processes = []

    def complete_ability(self, index):
        victim = self.processes[index]['receiver']
        del self.processes[index]
        return victim

    def use_ability(self, quiz, attacker, receiver, type):
        ability = {}
        if type == 0:
            ability = {
                'type': self.type[type],
                'quiz': quiz,
                'attacker': attacker,
                'receiver': receiver,
            }

        self.processes.append(ability)
        return len(self.processes)

    def check_user_state(self, quiz_id, user_id):
        user = [x for x in self.processes if self.processes['receiver'] == user_id and self.processes['quiz'] == quiz_id]

        return user


class FunnQuizManager:
    def __init__(self):
        self.rooms = {}
        self.abilityManager = AbilityManager()

    def __create_quiz(self, room_id):
        if room_id not in self.rooms:
            quiz = db.quizs.find_one({'_id': room_id})

            if quiz is None:
                return False

            self.rooms[room_id] = {
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

            return True
    
    def get_all_users(self, quizId):
        return list(self.rooms[quizId]['userStates'].keys())

    def join_room(self, room_id, user_id):

        flag = False
        if room_id not in self.rooms:
            flag = self.__create_quiz(room_id)

        if flag == False:
            return flag

        username = db.users.find_one({'_id': user_id})['username']
        self.rooms[room_id]['userStates'][user_id] = {
            'score': 0,
            'records': {},
        }
        join_room(room_id)
        return (flag, username)
        

    def start_quiz(self, quizId, questionId, questionCount):
        if quizId in self.rooms:
            question = self.rooms[quizId]['question']
            question['current_id'] = questionId
            self.rooms[quizId]['count'] = questionCount

    def finish_quiz(self, room_id):
        if room_id in self.rooms:
            if self.rooms[room_id]['count'] == self.rooms[room_id]['question']['current_index']:
                del self.rooms[room_id]

    def finish_question(self, quizId, userId, userAnswer=None, score=0, nextQuestionId=None):
        if quizId in self.rooms:
            if self.rooms[quizId]['count'] == 0:
                return False
            users = self.rooms[quizId]['userStates']
            question = self.rooms[quizId]['question']
            questionId = question['current_id']

            users[userId]['records'][questionId] = userAnswer
            users[userId]['score'] += score

            if question['received'] == len(self.rooms[quizId]['userStates']):
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
    
    def use_ability(self, quiz, attacker, receiver, type):
        index = self.abilityManager.use_ability(quiz, attacker, receiver, type)
        if type != 0:
            return -1
        return index

    def complete_ability(self, index):
        return self.abilityManager.complete_ability(index)

