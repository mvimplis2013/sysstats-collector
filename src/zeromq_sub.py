#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time

context = zmq.Context()
#context = zmq.Context.instance()

#  Socket to talk to server
print("Connecting to Diamond Data Collector Engine ...")

#socket = context.socket(zmq.REQ)
socket = context.socket(zmq.SUB)
#socket = context.socket(zmq.PULL)

<<<<<<< HEAD
#socket.connect("tcp://localhost:5555")
socket.connect("tcp://127.0.0.1:5556")
#socket.setsockopt(zmq.SUBSCRIBE, b'')
=======
socket.connect("tcp://127.0.0.1:5555")
#socket.bind("tcp://127.0.0.1:5555")
socket.setsockopt(zmq.SUBSCRIBE, b"")
>>>>>>> 450ba17000e6de80cf3f901233518d625ceeef1d

ctx = zmq.Context.instance()
s = ctx.socket(zmq.REQ)
s.connect("tcp://127.0.0.1:5556")
s.send(b"READY")
c = s.recv()
print("Receive Done:", c)

#socket.connect("ipc:///tmp/zmqtest")
#time.sleep(10)
while True:
    s.send(b"READY")
    c = s.recv()
    print("Receive Done:", c)

    o = socket.recv_pyobj()
    print('Done', o)
    #time.sleep(1)
#  Do 10 requests, waiting each time for a response
<<<<<<< HEAD
for update in range(10):
    print("Team")
    #  Get the reply.
    message = socket.recv_pyobj()
    #message = socket.recv_string()
    print("Received message:")
=======
"""for update in range(10):
    #  Get the reply.
    message = socket.recv_pyobj()
    #time.sleep(1)
    print("Received message:", message)"""
>>>>>>> 450ba17000e6de80cf3f901233518d625ceeef1d
