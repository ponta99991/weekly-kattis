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
try:
  import cPickle as pickle
except:
  import pickle

import socket

print_lock = threading.Lock()

def save_leaderboard(leaderboard):
    if(os.path.exists("./leaderboard.txt")):
        file = open("./leaderboard.txt", "rb+")
    else:
        file = open("./leaderboard.txt", "wb")

    pickle.dump(leaderboard, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    #file.write(serialized_leaderboard)
    file.close()

def load_leaderboard():
    if(not os.path.exists("./leaderboard.txt")):
        return None
    file = open("leaderboard.txt", "rb")
    
    #serialized_leaderboard = file.read()
    leaderboard = pickle.load(file)

    file.close()

    return leaderboard


def get_option(client, packet):
    global leaderboard
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

    if(packet.content == "add_to_leaderboard"):
        i = 0
        for user in leaderboard[packet.index].user:
            if packet.data.username == user.username:
                print("User already added, overwriting")
                leaderboard[packet.index].user[i] = packet.data
                save_leaderboard(leaderboard)
                return
            i += 1
        
        leaderboard[packet.index].user.append(packet.data)
        save_leaderboard(leaderboard)





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


# def generate_weekly():
#     all_problems = kattis.problems_ordered(37)
#     print("Done")

# generate_weekly()

#Increases recursion to handle pickling better
sys.setrecursionlimit(3000)

this_weeks_problem = []
this_weeks_problem.append("hello")
this_weeks_problem.append("vacuumba")
this_weeks_problem.append("knightjump")
#kattis.problem(this_weeks_problem)

# leaderboard = []
# leaderboard.append(common.Leaderboard(task=this_weeks_problem[0], user=[]))
# leaderboard.append(common.Leaderboard(task=this_weeks_problem[1], user=[]))
# leaderboard.append(common.Leaderboard(task=this_weeks_problem[2], user=[]))
# leaderboard[0].user.append(common.User(username="Strobe", lang="C#", time="3", date=time.time()))
# leaderboard[0].user.append(common.User(username="Kim", lang="Python3", time="5.2", date=time.time()-1069))
# leaderboard[0].user.append(common.User(username="Pukk", lang="Lua", time="2.4", date=time.time()-99999))
#save_leaderboard(leaderboard)

leaderboard = load_leaderboard()
if(leaderboard == None):
    leaderboard = []
    for i in range(3):
        leaderboard.append(common.Leaderboard(task=this_weeks_problem[i], user=[]))

# user.append(common.Leaderboard(username="Strobe", score="50", time="3", date=time.localtime()))
# user.append(common.Leaderboard(username="Kim", score="110", time="5.2", date=time.localtime()-1069))
# user.append(common.Leaderboard(username="Pukk", score="100", time="2.4", date=time.localtime()-99999))



start_server()