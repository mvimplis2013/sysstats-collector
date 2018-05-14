#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to Diamond Data Collector Engine ...")

#socket = context.socket(zmq.REQ)
socket = context.socket(zmq.SUB)

#socket.connect("tcp://localhost:5555")
socket.connect("tcp://127.0.0.1:5556")
#socket.setsockopt(zmq.SUBSCRIBE, b'')

#  Do 10 requests, waiting each time for a response
for update in range(10):
    print("Team")
    #  Get the reply.
    message = socket.recv_pyobj()
    #message = socket.recv_string()
    print("Received message:")
