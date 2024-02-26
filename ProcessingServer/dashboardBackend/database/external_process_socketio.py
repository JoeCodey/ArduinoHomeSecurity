from flask_socketio import SocketIO, namespace
from utilities.logger import get_logger_obj
import time 

log = get_logger_obj()



def send_external_socketio_event(socketio_external=None): 
    socketio_external.emit('test_response', 'from_external_process.py', namespace='/socket.io')

def send_external_socketio_event_thread(socketio_external=None): 
    log.majorcheckpoint("WE ARE IN AN EXTERNAL THREAD !!")
    if socketio_external is None:
        socketio_external = SocketIO(message_queue='redis://redis:6379')
    time.sleep(4)
    for i in range(0,10):
        time.sleep(3)
        socketio_external.emit('test_response', 'THREAD_from_external_process.py', namespace='/socket.io')


