from lib import problems as kattis
from lib import auth as kattis_auth
from lib import auth
from lib import communication as network
from lib import common
import base64
import os
import tkinter as tk
import tkinter.ttk as tkimage
import tkinter.messagebox
import time
import sys
import webbrowser
from PIL import ImageTk, Image  
import struct
from collections import namedtuple

from cryptography.fernet import Fernet
import getpass

WINDOW_W = 800
WINDOW_H = 600

def callback(url):
    webbrowser.open_new(url)

def save_credentials(username, password):
    #print("Enter username: ")
    #username = input()
    # try:
    #     password = getpass.getpass()
    # except Exception as error:
    #     print('ERROR', error)
    #     exit(-1)

    if(os.path.exists("./user_credencials.txt")):
        file = open("./user_credencials.txt", "r+")
        file.readline()
        if file.readline() == username + "\n":
            file.close()
            return
        else:
            file.seek(0)
    else:
        file = open("./user_credencials.txt", "w")

    key = Fernet.generate_key()
    fernet = Fernet(key)

    file.write(key.decode() + '\n')
    file.write(username + '\n')
    file.write(fernet.encrypt(password.encode()).decode())
    file.close()
    os.system( "attrib +h user_credencials.txt" )

def load_credentials():
    if(not os.path.exists("./user_credencials.txt")):
        return
    file = open("user_credencials.txt", "r")
    line = file.read().splitlines()
    
    fernet = Fernet(line[0])
    username = line[1]
    password = fernet.decrypt(line[2])
    username_field.insert(0, username) 
    password_field.insert(0, password)
    file.close()
    #return [username, password]

is_logged_in_on_kattis = False
def on_login():
    global username
    username = username_field.get()
    password = password_field.get()
    if(len(username) < 1 or len(password) < 1):
        tkinter.messagebox.showinfo("Error!", "Enter your credentials")
        return
    
    global kattis_user
    kattis_user = kattis_auth.auth(username, password)

    if(kattis_user == 0):
        tkinter.messagebox.showinfo("Error!", "Incorrect username or password!")
        return

    if(save_credentials_checkbox.get()):
        save_credentials(username, password)
        #print("Saving!")
    

    clearFrame(frame_login)
    global is_logged_in_on_kattis
    is_logged_in_on_kattis = True
    #Login frame
    global kattis_user_stats
    kattis_user_stats = kattis_user.stats()
    tk.Label(frame_login, text="Logged in as: \n" + kattis_user.username).grid(row=0, column=0)
    tk.Label(frame_login, text="Score: " + kattis_user_stats['score']).grid(row=1, column=0)
    tk.Label(frame_login, text="Rank: #" + kattis_user_stats['rank']).grid(row=2, column=0)

    if is_connected_to_server:
        create_validator()
    #print(kattis_user.stats())

# def on_load_credentials():
#     [username, password] = load_credentials()
#     username_field.insert(0, username) 
#     password = password_field.insert(0, password)

def clearFrame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    #window.forget()


def on_check_for_solution():
    network.send_string(server, "get_this_weeks_problem")
    ans = network.recieve_string(server)
    

# def create_menu():
#     connect_frame = tk.LabelFrame(text="Specify the destination you want to connect to").place(x=WINDOW_W/2, y=WINDOW_H/2-20)
#     tk.Label(text="Host Name (or IP address)").pack()
#     tk.Label(text="Port").pack()
#     global ip_field
#     ip_field = tk.Entry(connect_frame)
#     #ip_field.insert(0, "strobeindustries.net")
#     ip_field.insert(0, "192.168.1.100")
#     ip_field.pack()
#     global port_field
#     port_field = tk.Entry(connect_frame)
#     port_field.insert(0, "7778")
#     port_field.pack()
#     tk.Button(connect_frame, text="Connect", command=on_connect).pack()
    
#     global connection_error_field
#     connection_error_text = ""
#     connection_error_field = tk.Label(connect_frame, foreground="red", textvariable=connection_error_text)
#     connection_error_field.pack()
is_connected_to_server = False
def on_connect():
    global server
    [connection_established, server] = network.connect(ip_field.get(), int(port_field.get()))
    if not connection_established == 0:
        connection_error_field.config(text = "Connection error...")
        return

    #server.settimeout(1)

    global is_connected_to_server
    is_connected_to_server = True
    clearFrame(frame_connect)
    # information_frame = tk.LabelFrame(window, text="This Weeks Problem").place(x=WINDOW_W/2, y=0)
    # this_weeks_problem = get_problem()
    # problem_label = tk.Label(information_frame, text=this_weeks_problem, fg="blue", cursor="hand2")
    # problem_label.pack()
    # this_weeks_problem_page = kattis.problem(this_weeks_problem)
    # print(this_weeks_problem_page)
    # problem_label.bind("<Button-1>", lambda e: callback(this_weeks_problem_page['url']))
    #clearFrame(window)

    create_choose_task()

    if(is_logged_in_on_kattis):
        create_validator()



def create_choose_task():
    frame_choose_task = tk.LabelFrame(frame_sidebar, text="Choose Task" , bg="lime")
    frame_choose_task.grid(row=2, column=0, padx=5, pady=5, sticky="e,w")
    #frame_choose_task.grid_propagate(0)
    
    global button_task 
    button_task = []
    image_photo = []
    image_button = [Image.open('res/easy.png'), Image.open('res/mid.png'), Image.open('res/hard.png')]
    for i in range(3):
        image_photo.append(ImageTk.PhotoImage(image_button[i]))
        button = tkinter.Button(frame_choose_task, image=image_photo[i], command= lambda c=i: on_show_task(c), width=50, height=50)
        button.image = image_photo[i]
        button_task.append(button)
        button.grid(row=i, column=0, padx=5, pady=5, sticky="w,e")

    # img_1 = Image.open("res/easy.png")
    # photo_1 = ImageTk.PhotoImage(img_1)
    # label_photo_1 = tkinter.Label(frame_challenge_1, image=photo_1)
    # label_photo_1.image = photo_1
    # label_photo_1.grid(row=0, column=0)

def on_validation():
    if not ('current_displayed_leaderboard' in globals()):
        tkinter.messagebox.showinfo("Please!", "Choose an exercise to validate!")
        return

    [success, date, runtime, lang] = kattis_user.problem(current_displayed_leaderboard.task)
    if(success == False):
        tkinter.messagebox.showinfo("Cheating!", "You need to complete the exercise!")
        return

    #Remember:
    #Add answer for when person have been added maybee
    #Atleast add check on server so user is not dublicated.
    #No add check if user already is uploaded to leaderboard in client.
    
    #By some reason the complete html is transmitted? KAttis html
    new_user = common.User(username=username, date=date, time=runtime, lang=lang)
    #new_user = common.User(username = "a", lang="b", time="c", date=33)
    #packet = network.Packet(request=True, content="add_to_leaderboard", data=new_user, index=1)
    packet = network.Packet(request=True, content="add_to_leaderboard", data=new_user, index=leaderboard_index)
    print(packet.__sizeof__())
    network.send_packet(server, packet)

    print(leaderboard_index)
    leaderboard = get_leaderboard(leaderboard_index)
    display_leaderboard(frame_leaderboard, leaderboard)
    
    clearFrame(frame_validator)

    tk.Label(frame_validator, text="Validated!").pack()


def create_validator():
    global frame_validator
    frame_validator = tk.LabelFrame(frame_sidebar, text="Validate")
    frame_validator.grid(row=3, column=0, sticky="e, w")
    global validate_button
    validate_button = tk.Button(frame_validator, text="Validate Submission", command=on_validation)
    validate_button.pack()


def create_interface():
    global frame_sidebar
    frame_sidebar = tk.Frame(window, width=WINDOW_W/5, height=WINDOW_H, bg="purple")
    frame_sidebar.grid(row=0, column=0, sticky="nsew")#, padx=10, pady=5)
    #frame_sidebar.grid_propagate(0)

    global frame_leaderboard
    frame_leaderboard = tk.Frame(window, width=WINDOW_W*4/5, height=WINDOW_H, bg="green")
    frame_leaderboard.grid(row=0, column=1)

    global frame_connect
    frame_connect = tk.LabelFrame(frame_sidebar, text="Connect" , width=WINDOW_W/5, height=WINDOW_H*2/5, bg="red")
    frame_connect.grid(row=1, column=0, padx=5, pady=5)

    global frame_login
    frame_login = tk.LabelFrame(frame_sidebar, text="Login", width=WINDOW_W/5, height=WINDOW_H*3/5, bg="yellow")
    frame_login.grid(row=0, column=0, padx=5, pady=5)

    #Connect frame
    #connect_frame = tk.LabelFrame(text="Specify the destination you want to connect to").place(x=WINDOW_W/2, y=WINDOW_H/2-20)
    tk.Label(frame_connect, text="Host Name").grid(row=0, column=0)
    global ip_field
    ip_field = tk.Entry(frame_connect)
    ip_field.insert(0, "192.168.1.100")
    ip_field.grid(row=1, column=0)
    #ip_field.insert(0, "strobeindustries.net")
    tk.Label(frame_connect, text="Port").grid(row=2, column=0)
    global port_field
    port_field = tk.Entry(frame_connect)
    port_field.insert(0, "7778")
    port_field.grid(row=3, column=0)
    tk.Button(frame_connect, text="Connect", command=on_connect).grid(row=4, column=0)
    
    global connection_error_field
    connection_error_text = ""
    connection_error_field = tk.Label(frame_connect, foreground="red", textvariable=connection_error_text)
    connection_error_field.grid(row=5, column=0)


    #Login frame
    #frame_login = tk.LabelFrame(text="Enter your Kattis credentials").pack()#place(x=WINDOW_W/2, y=WINDOW_H/2-20)
    tk.Label(frame_login, text="Username").grid(row=0, column=0)
    tk.Label(text="Password")
    global username_field
    username_field = tk.Entry(frame_login)
    username_field.grid(row=1, column=0)
    global password_field
    password_field = tk.Entry(frame_login, show='*')
    password_field.grid(row=2, column=0)
    #tk.Button(frame_login, text="Load Credentials", command=on_load_credentials).grid(row=3, column=0)
    global save_credentials_checkbox
    save_credentials_checkbox = tk.IntVar()
    save_checkbox = tk.Checkbutton(frame_login, text="Save password", variable=save_credentials_checkbox)
    save_checkbox.grid(row=4, column=0)
    if(os.path.exists("./user_credencials.txt")):
        save_checkbox.toggle()
    tk.Button(frame_login, text="Login", command=on_login).grid(row=5, column=0)
    load_credentials()

    #When logged in and connected

def on_show_task(task_number):
    print(task_number)
    leaderboard = get_leaderboard(task_number)
    display_leaderboard(frame_leaderboard, leaderboard)


def get_leaderboard(i):
    global leaderboard_index
    leaderboard_index = i
    problemRequest = network.Packet(request=True, content="get_leaderboard", index=leaderboard_index)
    network.send_packet(server, problemRequest)
    packet = network.recieve_packet(server)
    leaderboard = packet.data
    print(leaderboard.task)
    return leaderboard

def display_leaderboard(frame_leaderboard, leaderboard):
    clearFrame(frame_leaderboard)
    frame_title = tk.Frame(frame_leaderboard, bg="orange")
    frame_title.grid(row=0, column=0, padx=5, pady=5)
    
    global current_displayed_leaderboard
    current_displayed_leaderboard = leaderboard
    kattis_task = kattis.problem(leaderboard.task)
    print(kattis_task)
    problem_label = tk.Label(frame_title, text=kattis_task["title"], fg="blue", cursor="hand2")
    problem_label.pack()
    problem_label.bind("<Button-1>", lambda e: callback(kattis_task['url']))
    #tk.Label(frame_title, text=leaderboard.task).pack()


    frame_header = tk.Frame(frame_leaderboard, bg="yellow")
    frame_header.grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame_header, text="Username").grid(row=0, column=0)
    tk.Label(frame_header, text="Time").grid(row=0, column=1)
    tk.Label(frame_header, text="Lang").grid(row=0, column=2)
    tk.Label(frame_header, text="Date").grid(row=0, column=3)

    frame_list = tk.Frame(frame_leaderboard, bg="green")
    frame_list.grid(row=2, column=0, padx=5, pady=5)

    print(leaderboard.user)
    if len(leaderboard.user) == 0:
        tk.Label(frame_leaderboard, text="No one have completed the task yet").grid(row=3, column=0)
        return
    
    for i in range(len(leaderboard.user)):
        leaderboard_user_field = tk.Frame(frame_list, height=20)
        leaderboard_user_field.grid(row=i, column=0)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].username).grid(row=0, column=0)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].time).grid(row=0, column=1)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].lang).grid(row=0, column=2)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].date).grid(row=0, column=3)


def get_problem():
    problemRequest = network.Packet(request=True, content="get_weekly")
    network.send_packet(server, problemRequest)
    packet = network.recieve_packet(server)
    print(packet.data)
    return packet.data

def on_closing():
    sys.exit()

#Increases recursion to handle pickling better
sys.setrecursionlimit(3000)

window = tk.Tk()
window.title("Strobe's Kattis Client")
#window.geometry('{0}x{1}'.format(str(WINDOW_W), str(WINDOW_H)))
window.protocol("WM_DELETE_WINDOW", on_closing)
#login_menu()
#create_menu()
create_interface()

#kattis.problem("listgame")

window.mainloop()
