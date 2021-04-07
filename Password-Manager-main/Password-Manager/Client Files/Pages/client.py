'''
Note: This client was made using a tutoral on the subject. This tutorial helped to create the sending to server
a link to the tutorial will be bellow
https://www.techwithtim.net/tutorials/socket-programming/
'''

import socket
import sys
import json

#sys.path.append('./')
#sys.path.append('./Pages')
#sys.path.append('./Pages/Helper_Functions')
sys.path.append('./Helper_Functions')
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


def send (code,first=None,second=None,third=None, four=None):
    '''
    This function takes up to 3 different varriables to send. Ones that need less have a NULL value.
    code - which service you want to access
    first - stores the first value the user wants to send
    second - stores the second value the user wants to send
    third - stores the third value the user wants to send
    four - stores the fourth value the user wants to send
    '''
    #What is being sent
    message = {
        "CODE":code,
        "FIR":first ,
        "SEC":second,
        "THR":third,
        "FOR":four
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
    result = send(ApplicationStates.SIGN_UP.value,user,pas)
    return result['Tag']

def login(user,pas):
    '''
    This program is for logining into an account
    user - the username of the account
    pas - the password of the account
    
    returns:
    0 - This means there is an error
    1 - The login was successful
    2 - Already logged into an account
    '''
    result =  send(ApplicationStates.LOGIN.value,user,pas)
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
    Array[i][3] - Hashed Password for that service
    '''
    result = send(ApplicationStates.GET_SERVICES.value)
    if (result["Tag"] == 0):
       return 0
    return result['senddata']


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


def check_service(sID):
    '''
    Get the password for this service
    
    Requires:
    sID - Service ID
    
    returns:
    0 - The account is not logged in
    2 - Logged in but an error
    info = {
        "ServiceID:service_id,
        "ServiceName": service_name,
        "Username": service_username,
        "Password": service_password
    } - this means that you successfully got recieved the account
    '''
    result = send(ApplicationStates.CHECK_SERVICE.value,sID)
    if (result['Tag'] == 1):
        info = {
        "ServiceID":result['ServiceID'],
        "ServiceName": result['ServiceName'],
        "Username": result['Username'],
        "Password": result['Password']
        }
        return info
    elif(result['Tag']==2 or result['Tag']==0):
        info = {
        "ServiceID":None,
        "ServiceName": None,
        "Username": None,
        "Password": None
        }
        return info
    return result

def update_service(sID,service_name=None,user=None,pas=None):
    '''
    Update the service
    
    Requirements
    sID - service ID
    service_name: change service name
    user - updated username gets None if there are no changes to be done
    pas - updated passwordgets None if there are no changes to be done
    
    Returns:
    0 - Error
    1 - Success
    '''
    result = send(ApplicationStates.UPDATE_SERVICE.value,sID,service_name, user,pas)
    if result['Tag'] == 0:
        return result['Tag']
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
    result = send(ApplicationStates.DELETE_SERVICE.value,sname)
    return result['Tag']

def delete_account():
    '''
    Delete account
    
    Requirements:
    None
    
    Returns:
    0 - Error
    1 - Succefully Deleted your account
    '''
    result = send(ApplicationStates.DELETE_ACCOUNT.value)
    return result['Tag']

def logout():
    '''
    This function is to logout of the account
    
    Returns
    0 - Not logged in
    1 - Success
    '''
    result = send(ApplicationStates.LOGOFF.value)
    return result['Tag']
def done():
    '''
    This function indicates that you are done using the program
    
    Returns:
    0 - Not logged in to an account
    1 - Success
    '''
    result = send(ApplicationStates.DISCONNECT.value)
    return result['Tag']
def ver():
    '''
    This function says which services that the user owns needs to be changed
    
    Returns
    {'Tag':0} - Error not logged in
    {'Tag':1,
    'Info':Array} - Success
    
    In the Array
    Array[i] - This sorts through the different services that need to be changed
    Array[i][0] - This is the service id
    Array[i][1] - This is the service name
    Array[i][2] - This is the service user name
    Array[i][3] - This is the service hased password
    Array[i][4] - If this is true it means that the password length is smaller than 6.
                    Otherwise this returns false
    Array[i][5] - This means that there is a repeat of this password in a different service
    '''
    result = send(ApplicationStates.VERIFY.value)
    return result

def send_account(rec_username,sevice_id):
    '''
    Sends the account
    
    Rec_username: the other account
    service_id: account want to send
    
    Result
    Tag = 0 not logged in.
    Tag:1 Password:password - password for other person
    Tag:2 recent an account to the same person
    Tag:3 sent to themselves
    Tag:4 user does not exist
    '''
    result = send(ApplicationStates.SEND_ACCOUNT.value,rec_username,sevice_id)
    return result
    
def rec_acc ():
    '''
    Gets all the sending requests
    
    Result
    Tag 0 - not logged in
    
    Tag 1 - success 
    Info - Array
    Info[i][0] - sending id
    info[i][1] -service_id
    info[i][2] -service_username
    info[i][3] -service_name
    '''
    result = send(ApplicationStates.RECIEVE_ACCOUNTS.value)
    return result

def rec_acc_pass(rec_username,sevice_id,password):
    '''
    
    Send username
    service_id
    Password you think it is
    
    Recieve
    0 - not logged in
    1 - success
    2 - failed password
    '''
    result = send(ApplicationStates.RECIEVE_ACCOUNT_PASSWORD.value,rec_username,sevice_id,password)
    return result

def get_send_pass(rec_user,service_id):
    '''
    Get your sending passwords
    
    Send
    Rec_username
    service_id
    
    Recieve:
    Tag: 0 - not logged in
    
    Tag:1 success
    Info:Array
    Array[i][0] - password for your sending
    '''
    result = send(ApplicationStates.RECIEVE_ACCOUNT_PASSWORD.value,rec_user,service_id)
    return result



if __name__ == "__main__":
    #Testing area 
    # print(setup("Dad","Bod"))
    # print(setup("Jack","ASDF"))
    # print((login('Jack','ASDF')))
    # print((login('Dad','Bod')))
    # print((send(23,'Jack',1)))
    # print(add_service("A","LOL",'ASDFGH'))
    # print(send(20,"DAD",4))
    # print((deleteService(1)))
    # print(send(20,"Jack",6))
    # print(send(24))
    # print(send(21))
    # print(send(22,'Dad',1,"KD3P8BWw$q\\wMNKZ6SY-9Eivh"))
    # print(send(21))

    # print(deleteService(31))
    # print(get_services())
    # print(update_service(32,"A","V","D"))
    # print(get_services())
    # print(check_service(32))

    # print(get_services())
    # print(check_service(1))
    # print(delete_account())
    # print(ver())
    print(done())
