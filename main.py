from QuizBankBackend import create_app
# from QuizBankBackend.funnyQuiz.event import socketio

app, socketio = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, log_output=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
