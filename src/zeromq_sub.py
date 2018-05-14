#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import time

#context = zmq.Context()
context = zmq.Context()

#  Socket to talk to server
print("Connecting to Diamond Data Collector Engine ...")

#socket = context.socket(zmq.REQ)
socket = context.socket(zmq.SUB)
#socket = context.socket(zmq.PULL)

#socket.connect("tcp://localhost:5555")
socket.connect("tcp://localhost:1234")
socket.setsockopt(zmq.SUBSCRIBE, b"")

ctx = zmq.Context.instance()
s = ctx.socket(zmq.REQ)
s.connect("tcp://localhost:1235")
s.send(b"READY")
s.recv()

#socket.connect("ipc:///tmp/zmqtest")
#time.sleep(10)
while True:
    o = socket.recv_pyobj()
    print('Done', o)
#  Do 10 requests, waiting each time for a response
"""for update in range(10):
    #  Get the reply.
    message = socket.recv_pyobj()
    #time.sleep(1)
    print("Received message:", message)"""
