
from utilities.logger import get_logger_obj

class MyClass:
    def __init__(self, socketio):
        self.socketio = socketio
    

def emmit_event_external_process(socketio):
    log = get_logger_obj()
    log.info("emmit_event_external_process")
    socketio.emit('new_data_from_server', 'websockettest.py ... ', namespace='/socket.io')
    

