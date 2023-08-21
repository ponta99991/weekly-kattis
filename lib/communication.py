import socket



def connect(host, port):

    destination = socket.socket()  # instantiate
    return [destination.connect_ex((host, port)), destination]



def send_string(destination, str):
    destination.send(str.encode())  # send message

def recieve_packet(destination):
    try:
        packet = destination.recv(1024)  # receive response
    except:
        return 0
    return packet

def recieve_string(destination):
    message = destination.recv(1024).decode()  # receive response
    return message

def terminate_connection(destination):
    destination.close()  # close the connection