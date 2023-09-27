from flask_socketio import join_room, leave_room
from QuizBankBackend.db import db


class ChatroomManager:
    def __init__(self):
        self.rooms = {}

    def join_chatroom(self, chatroomId, userId):
        if chatroomId not in self.rooms:
            self.rooms[chatroomId] = {
                'members': set(),
            }
        self.rooms[chatroomId]['members'].add(userId)
        join_room(chatroomId)

    def leave_chatroom(self, userId):
        if userId in self.rooms:
            self.rooms[userId]['members'].remove(userId)
            leave_room(userId)
            if len(self.rooms[userId]['members']) == 0:
                del self.rooms[userId]

    def get_all_users(self, userId):
        return list(self.rooms[userId]['members'])
    
    def send_message(self, chatroomId, message):
        if chatroomId in self.rooms:
            db.chatrooms.update_one(
                {'_id': chatroomId},
                {'$push': {'messages': message}}
            )
            return True

        return False

    def see_message(self, chatroomId, messageId, userId):
        if chatroomId in self.rooms:
            db.chatrooms.update_one(
                {'_id': chatroomId, 'messages._id': messageId},
                {'$addToSet': {'messages.$.seenBy': userId}}
            )
            return True

        return False