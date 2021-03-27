'''
Note: This client was made using a tutoral on the subject. This tutorial helped to create the sending to server
a link to the tutorial will be bellow
https://www.techwithtim.net/tutorials/socket-programming/
'''

import socket
import sys

sys.path.append('./Pages')
sys.path.append('./Pages/Helper_Functions')
import GeneratorPage as genPage

HEADER = 64
PORT = 3000
FORMAT = 'utf-8'
DISCONECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = # For connecting over internet put public adress ip
ADDRESS = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)


def send (msg):
    '''
    Example of sending a file from the client to the server
    
    '''
    #What is being sent
    message = {
        "CODE":'CODE',#Input a code that you want here
        "INFO":msg #input info here
    }
    # Send message
    message = msg.encode(FORMAT)
    msg_length = len(messsage)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    
    #Recieve Message
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
        print(msg)

def login(user,pas):
    '''
    This program is for logining into an account
    '''
    #What is being sent
    message = {
        "CODE":LOGIN,
        'USER':user,
        'PASS':pas
    }
    # Send message
    result = json.dumps(message)
    message = result.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    
    # Recieve message needs to be changed
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
        print(msg)#This needs to be changed currenty just outputs result to command line
        

def setup(user,pas1,pas2):
    '''
    This is for seting up a new user
    '''
    #What is being sent
    message = {
        "CODE":SETUP,
        'USER':user,
        'PASS1':pas,
        'PASS2':pas2
    }
    # Send message
    result = json.dumps(message)
    message = result.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

def done():
    '''
    This function indicates that you are done using the program
    '''
    #What is being sent
    message = {
        'CODE':DISCONECT_MESSAGE
    }
    # Send message
    result = json.dumps(message)
    message = result.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)

if __name__ == "__main__":
    genPage.screen()
    send(DISCONECT_MESSAGE)
