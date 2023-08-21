from lib import problems as kattis
from lib import auth as kattis_auth
from lib import auth
from lib import communication as network
import base64
import os
import tkinter as tk
import tkinter.messagebox
import time
import sys
import webbrowser
from PIL import ImageTk, Image  


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



def login_menu():
    login_frame = tk.LabelFrame(text="Enter your Kattis credentials").pack()#place(x=WINDOW_W/2, y=WINDOW_H/2-20)
    tk.Label(login_frame, text="Username").pack()
    tk.Label(text="Password")
    global username_field
    username_field = tk.Entry(login_frame)
    username_field.pack()
    global password_field
    password_field = tk.Entry(login_frame, show='*')
    password_field.pack()
    tk.Button(login_frame, text="Load Credentials", command=on_load_credentials).pack()
    global save_credentials_checkbox
    save_credentials_checkbox = tk.IntVar()
    tk.Checkbutton(text="Save password", variable=save_credentials_checkbox).pack()
    tk.Button(login_frame, text="Login", command=on_login).pack()

def clearFrame():
    # destroy all widgets from frame
    for widget in window.winfo_children():
       widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    #window.forget()

def get_problem():
    network.send_string(server, "get_this_weeks_problem")
    ans = network.recieve_string(server)
    print(ans)
    return ans

def on_check_for_solution():
    network.send_string(server, "get_this_weeks_problem")
    ans = network.recieve_string(server)
    

def create_menu():
    connect_frame = tk.LabelFrame(text="Specify the destination you want to connect to").place(x=WINDOW_W/2, y=WINDOW_H/2-20)
    tk.Label(text="Host Name (or IP address)").pack()
    tk.Label(text="Port").pack()
    global ip_field
    ip_field = tk.Entry(connect_frame)
    #ip_field.insert(0, "strobeindustries.net")
    ip_field.insert(0, "192.168.1.100")
    ip_field.pack()
    global port_field
    port_field = tk.Entry(connect_frame)
    port_field.insert(0, "7778")
    port_field.pack()
    tk.Button(connect_frame, text="Connect", command=on_connect).pack()
    
    global connection_error_field
    connection_error_text = ""
    connection_error_field = tk.Label(connect_frame, foreground="red", textvariable=connection_error_text)
    connection_error_field.pack()

def on_connect():
    global server
    [success, server] = network.connect(ip_field.get(), int(port_field.get()))
    if not success == 0:
        connection_error_field.config(text = "Connection error...")
        return

    clearFrame()

    option_frame = tk.LabelFrame(window, text="Options").place(x=WINDOW_W/2, y=WINDOW_H/2)
    
    information_frame = tk.LabelFrame(window, text="This Weeks Problem").place(x=WINDOW_W/2, y=0)
    
    this_weeks_problem = get_problem()
    problem_label = tk.Label(information_frame, text=this_weeks_problem, fg="blue", cursor="hand2")
    problem_label.pack()
    this_weeks_problem_page = kattis.problem(this_weeks_problem)
    print(this_weeks_problem_page)
    problem_label.bind("<Button-1>", lambda e: callback(this_weeks_problem_page['url']))

    #tk.Button(option_frame, text="Check for solution", command=on_check_for_solution).pack()

    #leaderboard = tk.LabelFrame(text="Options").place(x=0, y=0)



def nice_interface():
    frame_sidebar = tk.Frame(window, width=WINDOW_W/5, height=WINDOW_H, bg="purple")
    frame_sidebar.grid(row=0, column=0, sticky="nsew")#, padx=10, pady=5)
    #frame_sidebar.grid_propagate(0)
    frame_info = tk.Frame(window, width=WINDOW_W*4/5, height=WINDOW_H, bg="green")
    frame_info.grid(row=0, column=1)

    frame_connect = tk.LabelFrame(frame_sidebar, text="Connect" , width=WINDOW_W/5, height=WINDOW_H*2/5, bg="red")
    frame_connect.grid(row=0, column=0, padx=5, pady=5)
    frame_login = tk.LabelFrame(frame_sidebar, text="Login", width=WINDOW_W/5, height=WINDOW_H*3/5, bg="yellow")
    frame_login.grid(row=1, column=0, padx=5, pady=5)

    frame_week = tk.Frame(frame_info, width=WINDOW_W*4/5, height=WINDOW_H*1/10, bg="orange")
    frame_week.pack_propagate(0)
    frame_week.grid(row=0, column=0, padx=5, pady=5)

    tk.Label(frame_week, text="Week 1").pack()


    frame_challenge_1 = tk.Frame(frame_info, width=WINDOW_W*4/5, height=WINDOW_H*3/10, bg="green")
    frame_challenge_1.grid_propagate(0)
    frame_challenge_1.grid(row=1, column=0, padx=5, pady=5)
    frame_challenge_2 = tk.Frame(frame_info, width=WINDOW_W*4/5, height=WINDOW_H*3/10, bg="yellow")
    frame_challenge_2.grid_propagate(0)
    frame_challenge_2.grid(row=2, column=0, padx=5, pady=5)
    frame_challenge_3 = tk.Frame(frame_info, width=WINDOW_W*4/5, height=WINDOW_H*3/10, bg="purple")
    frame_challenge_3.grid_propagate(0)
    frame_challenge_3.grid(row=3, column=0, padx=5, pady=5)
    
    img_1 = Image.open("res/easy.png")
    photo_1 = ImageTk.PhotoImage(img_1)
    label_photo_1 = tkinter.Label(frame_challenge_1, image=photo_1)
    label_photo_1.image = photo_1
    label_photo_1.grid(row=0, column=0)

    img_2 = Image.open("res/mid.png")
    photo_2 = ImageTk.PhotoImage(img_2)
    label_photo_2 = tkinter.Label(frame_challenge_2, image=photo_2)
    label_photo_2.image = photo_2
    label_photo_2.grid(row=0, column=0)

    img_3 = Image.open("res/hard.png")
    photo_3 = ImageTk.PhotoImage(img_3)
    label_photo_3 = tkinter.Label(frame_challenge_3, image=photo_3)
    label_photo_3.image = photo_3
    label_photo_3.grid(row=0, column=0)
    #When logged in and connected


def on_closing():
    sys.exit()


# greeting = tk.Label(text="Hello, Tkinter")
# greeting.pack()

window = tk.Tk()
window.title("Strobe's Kattis Client")
#window.geometry('{0}x{1}'.format(str(WINDOW_W), str(WINDOW_H)))
window.protocol("WM_DELETE_WINDOW", on_closing)




#login_menu()
#create_menu()
nice_interface()


window.mainloop()

tk.Label(window, text="Username").place(x=10, y=10)





tk.Label(window, text="Username").pack(side="left")
tk.Entry(window, bd=10).pack(side="right")
tk.Button(window, text="Save", command=save_credentials).pack()
tk.Button(window, text="Load", command=load_credentials).pack()


#problems = kattis.problems(2)
#print(problems)
#problem = kattis.problem('2048')
#print(problem)
