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
        #Recive a message from client
        msg_length = int(msg_length)
        msg = json.loads(client.recv(msg_length).decode(FORMAT)) 
        return msg


'''
Below here is just the setup for different services to send to the server
'''
def setup(user,pas):
    '''
    This is for seting up a new user
    user - the username of the new account
    pas1 - the password of the new account
    pas2 - the edit password of the new account
    '''
    result = send(ApplicationStates.SIGN_UP.value,user,pas,None)
    if result['Tag'] == 0:
        return result['Report']

def login(user,pas):
    '''
    This program is for logining into an account
    user - the username of the account
    pas - the password of the account
    '''
    result =  send(ApplicationStates.LOGIN.value,user,pas,None)
    if (result["Tag"] == 0)
       return result['Report']

def get_services():
    '''
    This is for getting services
    '''
    result = send(ApplicationStates.GET_SERVICES.value,None,None,None)
    if (result["Tag"] == 0)
       return result['Report']

def add_service(sname, user,pas):
    '''
    Add a new service to the account
    '''
    result = send(ApplicationStates.ADD_SERVICE.value,sname,user,pas)
    if (result["Tag"] == 0)
       return result['Report']

def check_service(sname):
    #Maybe shouldnt require us`ername and password?
    '''
    
    '''
    result = send(ApplicationStates.CHECK_SERVICE.value,sname,None,None)
    if (result["Tag"] == 0)
       return result['Report']

def update_service(sname,user,pas):
    '''
    Update the service
    '''
    result = send(ApplicationStates.UPDATE_SERVICE.value,sname,user,pas)
    if (result["Tag"] == 0)
       return result['Report']

def deleteService(sname):
    '''
    Delete a service
    '''
    result = send(ApplicationStates.DELETE_SERVICE.value,sname,None,None)
    if (result["Tag"] == 0)
       return result['Report']

def delete_account():
    '''
    Delete account
    '''
    result = send(ApplicationStates.DELETE_ACCOUNT.value,None,None,None)
    if (result["Tag"] == 0)
       return result['Report']

def done():
    '''
    This function indicates that you are done using the program
    '''
    
    result = send(ApplicationStates.DISCONNECT.value,None,None,None)
    if (result["Tag"] == 0)
       return result['Report']
    



if __name__ == "__main__":
    #Testing area 
    
    # print(setup("John","ASDF"))
    # print(login("John","ASDF"))
    # print(get_services())
    # print(add_service("Dog","LOL",'DOLL'))
    # print(update_service("Google","DO","ROW"))
    # print(check_service("Google"))
    # print(deleteService("Google"))
    # print(get_services())
    # print(delete_account())
    print('In')
    print(done())
    print('OUT')
