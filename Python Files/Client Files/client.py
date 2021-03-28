'''
Note: This client was made using a tutoral on the subject. This tutorial helped to create the sending to server
a link to the tutorial will be bellow
https://www.techwithtim.net/tutorials/socket-programming/
'''

import socket
import sys
import json

sys.path.append('./')
sys.path.append('./Pages')
sys.path.append('./Pages/Helper_Functions')
import GeneratorPage as genPage

from application_states import ApplicationStates


HEADER = 64
PORT = 3000
FORMAT = 'utf-8'
DISCONECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = # For connecting over internet put public adress ip
ADDRESS = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)


def send (code,first,second,third):
    '''
    This function takes up to 3 different varriables to send. Ones that need less have a NULL value.
    code - which service you want to access
    first - stores the first value the user wants to send
    second - stores the second value the user wants to send
    third - stores the third value the user wants to send
    '''
    #What is being sent
    message = {
        "CODE":code,
        "FIR":first ,
        "SEC":second,
        "THR":third
    }
    # Send message
    result = json.dumps(message)
    message = result.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    
    #Recieve Message
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
        #Change this out so that it send the result to the application
        print(msg)
        return msg #This way it can go back to the location and distribute it to where it needs to go


'''
Below here is just the setup for different services to send to the server
'''
def setup(user,pas1,pas2):
    '''
    This is for seting up a new user
    user - the username of the new account
    pas1 - the password of the new account
    pas2 - the edit password of the new account
    '''
    send(ApplicationStates.SIGN_UP.value,user,pas1,pas2)

def login(user,pas):
    '''
    This program is for logining into an account
    user - the username of the account
    pas - the password of the account
    '''
    send(ApplicationStates.LOGIN.value,user,pas,None)

def services():
    '''
    This is for getting services
    '''
    send(ApplicationStates.GET_SERVICES.value,None,None,None)

def add_service(sname, user,pas):
    '''
    Add a new service to the account
    '''
    send(ApplicationStates.ADD_SERVICE.value,sname,user,pas)

def check_service(sname,user,pas):
    '''
    '''
    send(ApplicationStates.CHECK_SERVICES.value,sname,user,pas)

def update_service(SNAME,user,pas):
    '''
    Update the service
    '''
    send(ApplicationStates.UPDATE_SERVICES.value,sname,user,pas)

def deleteService(sname):
    '''
    Delete a service
    '''
    send(ApplicationStates.GET_SERVICES.value,sname,None,None)

def delete_account():
    '''
    Delete account
    '''
    send(ApplicationStates.GET_SERVICES.value,None,None,None)

def disconnect():
    '''
    disconnect from the server
    '''
    send(ApplicationStates.DISCONNECT.value,None,None,None)

def done():
    '''
    This function indicates that you are done using the program
    '''
    send(ApplicationStates.DISCONNECT.value,None,None,None)



if __name__ == "__main__":
    #Testing area 
    
    # genPage.screen()
    # setup("John","ASDF","Test")
    # delete_account()
    done()
