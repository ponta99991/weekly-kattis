from lib import problems as kattis
from lib import auth
from lib import communication as network
import base64
import os
import tkinter as tk
import time
import sys

from cryptography.fernet import Fernet
import getpass
import threading
from _thread import *

import socket

print_lock = threading.Lock()
 



def get_option(client, message):
    print("Got the following message: " + message)
    if(message == "get_this_weeks_problem"):
        print("Sending..." + this_weeks_problem)
        network.send_string(client, this_weeks_problem)
    elif(message[0] == 'u'):
        #u username
        line = message.splitlines()
        line[0]




# thread function
def threaded(client):
    while True:
 
        # data received from client
        packet = network.recieve_packet(client)
        if packet == 0:
            print('Terminating')
            #print_lock.release()
             
            # lock released on exit
            break
        else:
            message = packet.decode()
            get_option(client, message)
            
        #network.send_string(client, message)
 
    # connection closed
    client.close()
 
 
def start_server():
    host = ""
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 7778
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()
 
        # lock acquired by client
        #print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


this_weeks_problem = "listgame"

#kattis.problem(this_weeks_problem)


start_server()
