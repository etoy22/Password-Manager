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
    
    Needs:
    user - the username of the new account
    pas - the password of the new account
    
    returns:
    0 - This means there is an error
    1 - The operation was successful
    2 - This means that the username already exists
    '''
    result = send(ApplicationStates.SIGN_UP.value,user,pas,None)
    return result['Tag']

def login(user,pas):
    '''
    This program is for logining into an account
    user - the username of the account
    pas - the password of the account
    
    returns:
    0 - This means there is an error
    1 - The login was successful
    '''
    result =  send(ApplicationStates.LOGIN.value,user,pas,None)
    return result["Tag"]

def get_services():
    '''
    This is for getting services
    
    Returns 
    0 - The account is not logged in
    Array - should have all current services
    will look like this 
    Array[i] - i repersents differnet services
    Array[i][0] - Service Id will not show up on the screen but is important this will be sent back to the server
    Array[i][1] - name of the service
    Array[i][2] - Username for that service
    '''
    result = send(ApplicationStates.GET_SERVICES.value,None,None,None)
    # if (result["Tag"] == 0):
    #    return result

def add_service(sname, user,pas):
    '''
    Add a new service to the account
    
    Requires:
    sname - Name of this service
    user - username for this service
    pas - password for this service
    
    Returns:
    0 - The account is not logged in
    1 - Success    
    '''
    result = send(ApplicationStates.ADD_SERVICE.value,sname,user,pas)
    return result['Tag']
    # if (result["Tag"] == 0)
    #    return result['Report']

def check_service(sID):
    '''
    Get the password for this service
    
    Requires:
    sID - Service ID
    
    returns:
    0 - The account is not logged in
    2 - Logged in but error
    info = {
        "Username": service_username,
        "Password": service_password.
        "ServiceName": service_name,
        "ServiceID:service_id
    } - this means that you successfully got recieved the account
    '''
    result = send(ApplicationStates.CHECK_SERVICE.value,sname,None,None)
    return result

def update_service(sID,user,pas):
    '''
    Update the service
    
    Requirements
    sID - service ID
    user - updated username gets None if there are no changes to be done
    pas - updated passwordgets None if there are no changes to be done
    
    Returns:
    0 - Error
    1 - Success
    '''
    result = send(ApplicationStates.UPDATE_SERVICE.value,sname,user,pas)
    return result

def deleteService(sname):
    '''
    Delete a service
    
    Requirements
    sID - service ID
    
    Returns:
    0 - Error
    1 - Success
    '''
    result = send(ApplicationStates.DELETE_SERVICE.value,sname,None,None)
    return result

def delete_account():
    '''
    Delete account
    
    Requirements:
    None
    
    Returns:
    0 - Error
    1 - Succefully Deleted your account
    '''
    result = send(ApplicationStates.DELETE_ACCOUNT.value,None,None,None)
    return result

def done():
    '''
    This function indicates that you are done using the program
    
    Returns:
    1 - Success
    '''
    
    result = send(ApplicationStates.DISCONNECT.value,None,None,None)
    return result

if __name__ == "__main__":
    #Testing area 
    
    # print(setup("John","ASDF"))
    # print(login("John","ASDF"))
    # print(get_services())
    # print(add_service("Dog","LOL",'DOLL'))
    # print(add_service("STOP","LOL",'DOLL'))
    # print(update_service("Google","DO","ROW"))
    # print(check_service("Google"))
    # print(deleteService("Google"))
    # print(get_services())
    # print(delete_account())
    print(done())
