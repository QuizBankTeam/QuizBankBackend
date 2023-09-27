from flask_socketio import Namespace, emit
from QuizBankBackend.chatroom.manager import ChatroomManager


chatroomManager = ChatroomManager()

class ChatroomNamespace(Namespace):
    def on_connect(self):
        emit('connected')

    def on_disconnect(self):
        emit('disconnected')

    def on_join_chatroom(self, chatroomId, userId):
        print(userId + ' join chatroom in ' + chatroomId)
        chatroomManager.join_chatroom(chatroomId, userId)
        userCount = len(chatroomManager.get_all_users(chatroomId))
        emit('joinChatroom', userCount, to=chatroomId)

    def on_leave_chatroom(self, chatroomId, userId):
        print(userId + ' leave chatroom in ' + chatroomId)
        chatroomManager.leave_chatroom(chatroomId, userId)
        userCount = len(chatroomManager.get_all_users(chatroomId))
        emit('leaveChatroom', userCount, to=chatroomId)

    def on_send_message(self, chatroomId, message):
        print('send message in ' + chatroomId)
        chatroomManager.send_message(chatroomId, message)
        emit('sendMessage', message, to=chatroomId)

    def on_see_message(self, chatroomId, messageId, userId):
        print('see message in ' + chatroomId)
        chatroomManager.see_message(chatroomId, messageId, userId)
        emit('seeMessage', messageId, to=chatroomId)