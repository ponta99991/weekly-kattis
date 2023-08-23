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
from lib import common

import socket

print_lock = threading.Lock()
 



def get_option(client, packet):

    #answer = network.Packet(request=False, content="default", data="default")
    print("Got the following packet: " + packet.content)
    if(packet.content == "get_weekly"):
        print("Sending..." + this_weeks_problem)
        answer = network.Packet(request=False, content="weekly", data=this_weeks_problem)
        network.send_packet(client, answer)

    if(packet.content == "get_leaderboard"):
        print("Sending leaderboard...")
        answer = network.Packet(request=False, content="leaderboard", data=leaderboard[packet.index])
        network.send_packet(client, answer)





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
            if packet.request == True:
                get_option(client, packet)
            
        #network.send_string(client, message)
 
    # connection closed
    client.close()
 
 
def start_server():
    host = ""
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 7778
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.settimeout(1)
    print("socket binded to port", port)
 
    # put the socket into listening mode
    server.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        while True:
            try:
                client, addr = server.accept()
            except:
                pass
            else:
                break

        # lock acquired by client
        #print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (client,))
    server.close()



this_weeks_problem = "listgame"

#kattis.problem(this_weeks_problem)

leaderboard = []
leaderboard.append(common.Leaderboard(task=this_weeks_problem, user=[]))
leaderboard[0].user.append(common.User(username="Strobe", score="50", time="3", date=time.time()))
leaderboard[0].user.append(common.User(username="Kim", score="110", time="5.2", date=time.time()-1069))
leaderboard[0].user.append(common.User(username="Pukk", score="100", time="2.4", date=time.time()-99999))

# user.append(common.Leaderboard(username="Strobe", score="50", time="3", date=time.localtime()))
# user.append(common.Leaderboard(username="Kim", score="110", time="5.2", date=time.localtime()-1069))
# user.append(common.Leaderboard(username="Pukk", score="100", time="2.4", date=time.localtime()-99999))
start_server()
