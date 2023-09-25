debug=True
bind='0.0.0.0:5000'
workers=1
thread=4
loglevel='debug'
# worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
worker_class = 'eventlet'
reload=True