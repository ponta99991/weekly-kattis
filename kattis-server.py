from lib import problems as kattis
from lib import auth
from lib import communication as network
import base64
import os
import tkinter as tk
import time
import datetime
import sys
import random

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

VERSION_NUMBER = "0.6"

print_lock = threading.Lock()

def save_leaderboard(filename, leaderboard):
    if(os.path.exists(filename)):
        file = open(filename, "rb+")
    else:
        file = open(filename, "wb")

    pickle.dump(leaderboard, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    #file.write(serialized_leaderboard)
    file.close()

def load_leaderboard(filename):
    if(not os.path.exists(filename)):
        return None
    file = open(filename, "rb")
    
    #serialized_leaderboard = file.read()
    leaderboard = pickle.load(file)

    file.close()

    return leaderboard


def get_option(client, packet):
    global leaderboard
    #answer = network.Packet(request=False, content="default", data="default")
    print("Got the following packet: " + packet.content)
    # if(packet.content == "get_weekly"):
    #     print("Sending..." + this_weeks_problem)
    #     answer = network.Packet(request=False, content="weekly", data=this_weeks_problem)
    #     network.send_packet(client, answer)

    #Check the clients version:
    if(packet.content == "validate_version"):
        print("Sending version...")
        answer = network.Packet(request=False, content="version", data=VERSION_NUMBER)
        network.send_packet(client, answer)
        if not packet.data == VERSION_NUMBER:
            print("Version of client is incorrect!\nTerminating connection...")
            client.close()
            sys.exit()
        print("Version validated!\n")


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
                save_leaderboard(leaderboard_filename, leaderboard)
                return
            i += 1
        
        leaderboard[packet.index].user.append(packet.data)
        save_leaderboard(leaderboard_filename, leaderboard)


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
    start_new_thread(update_weekly, (None,))
 
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

        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (client,))
    server.close()


def generate_weekly():
    [id, diff] = kattis.problems_ordered(37)
    #[id, diff] = kattis.problems_ordered()

    #Convert ranges to float
    for i in range(len(diff)):
        if(len(diff[i]) > 3):
            diff[i] = diff[i][6:]

    easy = []
    medium = []
    hard = []
    insane = []
    #Group
    for i in range(len(diff)):
        if(float(diff[i]) < 2):
            easy.append([id[i], diff[i]])
        elif(float(diff[i]) < 4):
            medium.append([id[i], diff[i]])
        elif(float(diff[i]) < 6):
            hard.append([id[i], diff[i]])
        else:
            insane.append([id[i], diff[i]])
    e = easy[random.randint(0,len(easy))][0]
    m = medium[random.randint(0,len(medium))][0]
    h = hard[random.randint(0,len(hard))][0]
    i = insane[random.randint(0,len(insane))][0]

    print("Done")

    return [e, m, h, i]

def update_weekly(no):
    global current_week
    global current_year
    global leaderboard
    while(True):
        time.sleep(15)
        test_week = datetime.datetime.now().isocalendar()[1]
        if(not current_week == test_week):
            test_year = datetime.datetime.now().isocalendar()[0]
            global leaderboard_filename
            leaderboard_filename = "./leaderboard_" + str(test_year) + "_" +str(test_week)+".txt"
            
            this_weeks_problem = generate_weekly()
            
            new_leaderboard = []
            for i in range(3):
                new_leaderboard.append(common.Leaderboard(task=this_weeks_problem[i], user=[]))
            save_leaderboard(leaderboard_filename, new_leaderboard)

            leaderboard = new_leaderboard
            current_week = test_week
            current_year = test_year
                

current_year = datetime.datetime.now().isocalendar()[0]
current_week = datetime.datetime.now().isocalendar()[1]

leaderboard_filename = "./leaderboard_" + str(current_year) + "_" +str(current_week)+".txt"
leaderboard = load_leaderboard(leaderboard_filename)

if(leaderboard == None):
    this_weeks_problem = generate_weekly()
    leaderboard = []
    for i in range(3):
        leaderboard.append(common.Leaderboard(task=this_weeks_problem[i], user=[]))
    save_leaderboard(leaderboard_filename, leaderboard)


start_server()



# this_weeks_problem = []
# this_weeks_problem.append("hello")
# this_weeks_problem.append("vacuumba")
# this_weeks_problem.append("knightjump")
#kattis.problem(this_weeks_problem)

# leaderboard = []
# leaderboard.append(common.Leaderboard(task=this_weeks_problem[0], user=[]))
# leaderboard.append(common.Leaderboard(task=this_weeks_problem[1], user=[]))
# leaderboard.append(common.Leaderboard(task=this_weeks_problem[2], user=[]))
# leaderboard[0].user.append(common.User(username="Strobe", lang="C#", time="3", date=time.time()))
# leaderboard[0].user.append(common.User(username="Kim", lang="Python3", time="5.2", date=time.time()-1069))
# leaderboard[0].user.append(common.User(username="Pukk", lang="Lua", time="2.4", date=time.time()-99999))
#save_leaderboard(leaderboard)

#if(leaderboard == None):
    

# user.append(common.Leaderboard(username="Strobe", score="50", time="3", date=time.localtime()))
# user.append(common.Leaderboard(username="Kim", score="110", time="5.2", date=time.localtime()-1069))
# user.append(common.Leaderboard(username="Pukk", score="100", time="2.4", date=time.localtime()-99999))


