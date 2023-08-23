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
    print("Enter username: ")
    #username = input()
    # try:
    #     password = getpass.getpass()
    # except Exception as error:
    #     print('ERROR', error)
    #     exit(-1)

    file = open("user_credencials", "w")
    key = Fernet.generate_key()
    fernet = Fernet(key)

    file.write(key.decode() + '\n')
    file.write(username + '\n')
    file.write(fernet.encrypt(password.encode()).decode())
    file.close()
    os.system( "attrib +h user_credencials" )

def load_credentials():
    file = open("user_credencials", "r")
    line = file.read().splitlines()
    
    fernet = Fernet(line[0])
    username = line[1]
    password = fernet.decrypt(line[2])
    return [username, password]

# if(not os.path.exists("./user_credencials")):
#     save_credentials()
# user = load_credentials()
#print(user)

def on_login():
    username = username_field.get()
    password = password_field.get()
    if(len(username) < 1 or len(password) < 1):
        tkinter.messagebox.showinfo("Error!", "Enter your credentials")
        return
    
    kattis_user = kattis_auth.auth(username, password)

    if(kattis_user == 0):
        tkinter.messagebox.showinfo("Error!", "Incorrect username or password!")
        return

    if(save_credentials_checkbox.get()):
        save_credentials(username, password)
        #print("Saving!")
    
    print(kattis_user.stats())

def on_load_credentials():
    [username, password] = load_credentials()
    username_field.insert(0, username) 
    password = password_field.insert(0, password)

# def login_menu():
#     login_frame = tk.LabelFrame(text="Enter your Kattis credentials").pack()#place(x=WINDOW_W/2, y=WINDOW_H/2-20)
#     tk.Label(login_frame, text="Username").pack()
#     tk.Label(text="Password")
#     global username_field
#     username_field = tk.Entry(login_frame)
#     username_field.pack()
#     global password_field
#     password_field = tk.Entry(login_frame, show='*')
#     password_field.pack()
#     tk.Button(login_frame, text="Load Credentials", command=on_load_credentials).pack()
#     global save_credentials_checkbox
#     save_credentials_checkbox = tk.IntVar()
#     tk.Checkbutton(text="Save password", variable=save_credentials_checkbox).pack()
#     tk.Button(login_frame, text="Login", command=on_login).pack()

def clearFrame():
    # destroy all widgets from frame
    for widget in window.winfo_children():
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

def on_connect():
    global server
    [success, server] = network.connect(ip_field.get(), int(port_field.get()))
    if not success == 0:
        connection_error_field.config(text = "Connection error...")
        return

    # information_frame = tk.LabelFrame(window, text="This Weeks Problem").place(x=WINDOW_W/2, y=0)
    # this_weeks_problem = get_problem()
    # problem_label = tk.Label(information_frame, text=this_weeks_problem, fg="blue", cursor="hand2")
    # problem_label.pack()
    # this_weeks_problem_page = kattis.problem(this_weeks_problem)
    # print(this_weeks_problem_page)
    # problem_label.bind("<Button-1>", lambda e: callback(this_weeks_problem_page['url']))
    #clearFrame()

    create_choose_task()

def on_show_task(task_number):
    print(task_number)
    leaderboard = get_leaderboard(task_number)
    display_leaderboard(frame_info, leaderboard)

def create_choose_task():
    frame_choose_task = tk.LabelFrame(frame_sidebar, text="Choose Task" , height=150, bg="lime")
    frame_choose_task.grid(row=2, column=0, padx=5, pady=5)
    
    global button_task 
    button_task = []
    image_photo = []
    image_button = [Image.open('res/easy.png'), Image.open('res/mid.png'), Image.open('res/hard.png')]
    for i in range(3):
        image_photo.append(ImageTk.PhotoImage(image_button[i]))
        button = tkinter.Button(frame_choose_task, image=image_photo[i], command= lambda c=i: on_show_task(c), width=50, height=50)
        button.image = image_photo[i]
        button_task.append(button)
        button.grid(row=i, column=0, padx=5, pady=5)

    # img_1 = Image.open("res/easy.png")
    # photo_1 = ImageTk.PhotoImage(img_1)
    # label_photo_1 = tkinter.Label(frame_challenge_1, image=photo_1)
    # label_photo_1.image = photo_1
    # label_photo_1.grid(row=0, column=0)


def create_interface():
    global frame_sidebar
    frame_sidebar = tk.Frame(window, width=WINDOW_W/5, height=WINDOW_H, bg="purple")
    frame_sidebar.grid(row=0, column=0, sticky="nsew")#, padx=10, pady=5)
    #frame_sidebar.grid_propagate(0)

    global frame_info
    frame_info = tk.Frame(window, width=WINDOW_W*4/5, height=WINDOW_H, bg="green")
    frame_info.grid(row=0, column=1)

    frame_connect = tk.LabelFrame(frame_sidebar, text="Connect" , width=WINDOW_W/5, height=WINDOW_H*2/5, bg="red")
    frame_connect.grid(row=1, column=0, padx=5, pady=5)

    frame_login = tk.LabelFrame(frame_sidebar, text="Login", width=WINDOW_W/5, height=WINDOW_H*3/5, bg="yellow")
    frame_login.grid(row=0, column=0, padx=5, pady=5)

    frame_week = tk.Frame(frame_info, width=WINDOW_W*4/5, height=WINDOW_H*1/10, bg="orange")
    frame_week.pack_propagate(0)
    frame_week.grid(row=0, column=0, padx=5, pady=5)

    tk.Label(frame_week, text="Week 1").pack()

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
    tk.Button(frame_login, text="Load Credentials", command=on_load_credentials).grid(row=3, column=0)
    global save_credentials_checkbox
    save_credentials_checkbox = tk.IntVar()
    tk.Checkbutton(frame_login, text="Save password", variable=save_credentials_checkbox).grid(row=4, column=0)
    tk.Button(frame_login, text="Login", command=on_login).grid(row=5, column=0)

    #When logged in and connected

def get_leaderboard(leaderboard_index):
    problemRequest = network.Packet(request=True, content="get_leaderboard", index=0)
    network.send_packet(server, problemRequest)
    packet = network.recieve_packet(server)
    leaderboard = packet.data
    print(leaderboard.task)
    return leaderboard

def display_leaderboard(field, leaderboard):
    
    for i in range(len(leaderboard.user)):
        leaderboard_user_field = tk.Frame(field, height=20)
        leaderboard_user_field.grid(row=i, column=0)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].username).grid(row=0, column=0)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].score).grid(row=0, column=1)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].time).grid(row=0, column=2)
        tk.Label(leaderboard_user_field, text=leaderboard.user[i].date).grid(row=0, column=3)

def get_problem():
    problemRequest = network.Packet(request=True, content="get_weekly")
    network.send_packet(server, problemRequest)
    packet = network.recieve_packet(server)
    print(packet.data)
    return packet.data

def on_closing():
    sys.exit()



window = tk.Tk()
window.title("Strobe's Kattis Client")
#window.geometry('{0}x{1}'.format(str(WINDOW_W), str(WINDOW_H)))
window.protocol("WM_DELETE_WINDOW", on_closing)
#login_menu()
#create_menu()
create_interface()


window.mainloop()
