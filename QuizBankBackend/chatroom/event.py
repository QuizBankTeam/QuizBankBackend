from QuizBankBackend import socketio
from QuizBankBackend.chatroom.namespace import ChatroomNamespace


socketio.on_namespace(ChatroomNamespace('/chatroom'))