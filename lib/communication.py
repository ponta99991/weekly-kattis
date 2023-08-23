import socket
from collections import namedtuple
import struct
try:
  import cPickle as pickle
except:
  import pickle
from dataclasses import dataclass

format_ = "6shhih50s2s"

class Packet:
    request: bool
    content: str
    data: str
    index: int

    def __init__(self, request, content, index = 0, data = "default"):
        self.request = request
        self.content = content
        self.index = index
        self.data = data

def connect(host, port):
    destination = socket.socket()  # instantiate
    return [destination.connect_ex((host, port)), destination]

def send_packet(destination, packet):
    string_to_send = pickle.dumps(packet)
    destination.send(string_to_send)  # send message

def send_string(destination, str):
    destination.send(str.encode())  # send message

def recieve_packet(destination):
    try:
        packet = pickle.loads(destination.recv(1024))
    except:
        return 0
    return packet

def recieve_string(destination):
    message = destination.recv(1024).decode()  # receive response
    return message

def terminate_connection(destination):
    destination.close()  # close the connection