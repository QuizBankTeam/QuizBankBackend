from flask_socketio import join_room, close_room, leave_room, rooms
from colorama import Fore, Back, Style
from flask import request
from QuizBankBackend.db import db
from QuizBankBackend.constant import *


# class AbilityManager:
#     def __init__(self):
#         self.type = ['stall']
#         self.processes = []

#     def complete_ability(self, index):
#         victim = self.processes[index]['receiver']
#         del self.processes[index]
#         return victim

#     def use_ability(self, quiz, attacker, receiver, type):
#         ability = {}
#         if type == 0:
#             ability = {
#                 'type': self.type[type],
#                 'quiz': quiz,
#                 'attacker': attacker,
#                 'receiver': receiver,
#             }

#         self.processes.append(ability)
#         return len(self.processes)

#     def check_user_state(self, quiz_id, user_id):
#         user = [x for x in self.processes if self.processes['receiver'] == user_id and self.processes['quiz'] == quiz_id]

#         return user


class FunnQuizManager:
    def __init__(self):
        self.socketPool = {}
        self.rooms = {}
        # self.abilityManager = AbilityManager()

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
        # print(Fore.RED + user_id + ' join quiz in ' + room_id + Style.RESET_ALL)
        # print(Fore.RED + self.rooms + Style.RESET_ALL)
        return list(self.rooms[quizId]['userStates'].keys())

    def get_all_quizs(self):
        return rooms(namespace='/funnyQuiz')

    def join_room(self, room_id, user_id):
        flag = True
        if room_id not in self.rooms:
            flag = self.__create_quiz(room_id)

        if flag == False:
            return flag, None

        self.rooms[room_id]['userStates'][user_id] = {
            'score': 0,
            'records': {},
        }
        self.socketPool[request.sid] = {
            'room_id': room_id,
            'user_id': user_id,
        }

        usersRaw = db.users.find({'_id': { '$in': list(self.rooms[room_id]['userStates'].keys())}})
        users = {}
        for user in usersRaw:
            users[user['_id']] = user['username']
        join_room(room_id)
        return (flag, users)
        
    def leave_room(self):
        sid = request.sid
        room_id = self.socketPool[sid]['room_id']
        user_id = self.socketPool[sid]['user_id']
        if room_id in self.rooms:
            del self.rooms[room_id]['userStates'][user_id]
            del self.socketPool[sid]
            leave_room(room_id)
            if len(self.rooms[room_id]['userStates']) == 0:
                close_room(room_id)
                del self.rooms[room_id]

    def start_quiz(self, quizId, questionId, questionCount):
        if quizId in self.rooms:
            question = self.rooms[quizId]['question']
            question['current_id'] = questionId
            self.rooms[quizId]['count'] = questionCount

    def finish_quiz(self, room_id):
        if room_id in self.rooms:
            if self.rooms[room_id]['count'] == self.rooms[room_id]['question']['current_index']:
                close_room(room_id)
                del self.rooms[room_id]

    def finish_question(self, quizId, userId, qtype, userAnswer=None, score=0, nextQuestionId=None):
        if quizId in self.rooms:
            if self.rooms[quizId]['count'] == 0:
                return False
            users = self.rooms[quizId]['userStates']
            question = self.rooms[quizId]['question']
            questionId = question['current_id']
            
            print(Fore.RED + questionId)
            print(nextQuestionId)
            if (qtype == 'MultipleChoiceS' or qtype == 'MultipleChoiceM' or qtype == 'TrueOrFalse') and type(userAnswer) is str:
                userAnswerList = userAnswer.strip('][').split(', ')
                users[userId]['records'][questionId] = userAnswerList
                print(str(userAnswerList))
            else:
                users[userId]['records'][questionId] = userAnswer

            print(Style.RESET_ALL)
            users[userId]['score'] += score

            question['received'] += 1

            if question['received'] >= len(self.rooms[quizId]['userStates']):
                question['current_id'] = nextQuestionId
                question['received'] = 0
                question['current_index'] += 1
                return True

            return False

    def get_quiz_state(self, room_id):
        if room_id in self.rooms:
            return self.rooms[room_id]
        return None
    
    # def use_ability(self, quiz, attacker, receiver, type):
    #     index = self.abilityManager.use_ability(quiz, attacker, receiver, type)
    #     if type != 0:
    #         return -1
    #     return index

    # def complete_ability(self, index):
    #     return self.abilityManager.complete_ability(index)