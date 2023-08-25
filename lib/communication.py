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

# def recieve_packet(destination):
#     #try:    while True:
#     try:
#         packet = destination.recv(100000)
#     except TimeoutError:
#         return 0
#     return pickle.loads(packet)

def recieve_packet(destination):
    #try:
    data = []
    while True:
        try:
            packet = destination.recv(1024)
        except:
            return 0
        
        data.append(packet)
        if not packet.__sizeof__() >= 1056:
            break
        #if not packet: 

    if len(data) == 1:
        packet = pickle.loads(packet)
        return packet
    assembled_packet = pickle.loads(b"".join(data))
    #packet = pickle.loads(destination.recv(1024))
    #except:
    #    return 0
    return assembled_packet

# def recieve_packet(destination):
#     #try:
#     data = []
#     while True:
#         print("Test")
#         try:
#             packet = destination.recv(1024)
#         except:
#             if(len(data) == 0):
#                 return 0
#             break
#         #if not packet: 
#         data.append(packet)
#     assembled_packet = pickle.loads(b"".join(data))
#     #packet = pickle.loads(destination.recv(1024))
#     #except:
#     #    return 0
#     return assembled_packet

def recieve_string(destination):
    message = destination.recv(4096).decode()  # receive response
    return message

def terminate_connection(destination):
    destination.close()  # close the connection