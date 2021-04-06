'''
Note: This server was made using a tutoral on the subject. This tutorial helped to create the main and the handleClient
a link to the tutorial will be bellow
https://www.techwithtim.net/tutorials/socket-programming/
'''

import socket
import threading
import sqlite3
import json

from Crypto.Random import get_random_bytes



from os import (path,pardir)

import encrypt

from database_functions import (add_service, add_user, check_data_from_service, create_database,
                                delete_service, delete_user, get_master_pwd, get_key,
                                get_user_id, get_usernames_list, list_saved_services,
                                update_service_password, update_service_username,
                                get_username,update_service_name)

from application_states import ApplicationStates

HEADER = 64
PORT = 3000
SERVER = socket.gethostbyname(socket.gethostname()) #Local Hosting
#SERVER =  # For connecting over internet put public adress ip one may have to deactivate there firewall for this to work
ADDRESS = (SERVER,PORT)
FORMAT = 'utf-8'

''' 
This will link the username that the user logs into with there IP.
This means that the user cannot gain access to another account on that IP address while logged into a different account
'''
account_tracker = dict()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def send_client(message):
    '''
    This is used to send a message from the server back to the client
    message - the message you want to send back to the client
    '''
    result = json.dumps(message)
    message = result.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    con.send(send_length)
    con.send(message)

def serverEncrypt(service_password, iv=None, cipher_key=None,mac_key=None):
    '''
    Encrypts the service password 
    
    Requires:
    service_username - the service username
    service_password - the service password
    adr - the address of the current user
    '''
    if iv == None:
        iv = get_random_bytes(16)
    if cipher_key == None:
        cipher_key = get_random_bytes(16)
    if mac_key == None:
        mac_key = get_random_bytes(16)
    ciphertext, tag = encrypt.encrypt_then_mac(service_password.encode(FORMAT),iv,cipher_key,mac_key)
    return ciphertext, tag, cipher_key, mac_key

def serverDecrypt(user_id,service_id):
    '''
    check_data_from_service needs to give tag as well
    '''
    ciphertext, tag, cipher_key, mac_key = check_data_from_service(user_id, service_id)
    service_password = encrypt.verify_then_decrypt(ciphertext, tag, cipher_key, mac_key)
    return str(service_password)[2:-1]

def handle_client(con,adr):
    '''
    This is where a client gets put while connected to the server
    con - connection to their computer
    adr - address of their computer
    '''
    print(f"[NEW CONNECTION] {adr} connected.")
    connected = True
    while connected:
        #decode message recived
        msg_length = con.recv(HEADER).decode(FORMAT)
        if msg_length:
            #Recive a message from client
            msg_length = int(msg_length)
            msg = json.loads(con.recv(msg_length).decode(FORMAT))         
           # SIGN_UP 
            if msg['CODE']== ApplicationStates.SIGN_UP.value:
                username = msg['FIR']
                password = msg['SEC']
                users_list = get_usernames_list()
                flip = True
                for name in users_list: 
                    if username == name[0]: 
                        # user already exist
                        flip = False
                        break
                if flip: 
                    try:
                        #password may be failing
                        add_user(username, password)
                        accessed = {
                            "Tag":1
                        }
                        send_client(accessed)
                    except sqlite3.Error:
                        accessed = {
                            "Tag":0,
                            "Report":"ERROR"
                        }
                        send_client(accessed)
                else:
                    accessed = {
                        "Tag":2,
                        "Report":"Already exist"
                    }
                    send_client(accessed)
            #Case if someone attempts to login
            elif msg['CODE'] == ApplicationStates.LOGIN.value:
                if adr not in account_tracker:
                #Change earlier than this so that it actually requires the username and passwords to be correct
                    username = msg['FIR']
                    password = msg['SEC']
                    #  Checking if user exists
                    users_list = get_usernames_list()
                    accessed = {
                        "Tag":0,
                        "Report":"Issue with username or password"
                    } #The username or password has an issue
                    for user in users_list:
                        if username == user[0]:
                            if password == get_master_pwd(username):
                                user_id = get_user_id(username)
                                account_tracker[adr] = user_id
                                accessed = {
                                    "Tag":1,
                                    "User_id":user_id
                                }
                                break
                    send_client(accessed)
                else:
                    accessed = {
                        'Tag':2,
                        "Report":"Second account loging in"
                    }
            # send service list
            elif msg['CODE'] == ApplicationStates.GET_SERVICES.value:
                if adr in account_tracker:
                    user_id = account_tracker[adr]
                    services_list = list_saved_services(user_id)
                    senddata = []
                    for i in range (len(services_list)):
                        listing = list(services_list[i])
                        listing[3] = str(listing)[2:-1]
                        senddata.append(listing)
                    accessed['senddata'] = senddata
                    accessed = {
                        "Tag":1,
                        "senddata": senddata
                    }
                    send_client(accessed)
                else:
                    accessed = {
                        "Tag":0,
                        "Report":"Error no account"
                    }
                    send_client(accessed)
            # add service to account
            elif msg['CODE'] == ApplicationStates.ADD_SERVICE.value:
                if adr in account_tracker:
                    service_name = msg['FIR']
                    service_username = msg['SEC']
                    service_password = msg['THR']
                    services_list = list_saved_services(account_tracker[adr])
                    user_id = account_tracker[adr]
                    ciphertext, tag, cipher_key, mac_key = serverEncrypt(service_password)
                    add_service(service_name, service_username,
                        ciphertext, user_id,tag, cipher_key, mac_key)
                    accessed = {
                         "Tag":1
                    }                    
                    send_client(accessed)  
                else:
                    accessed = {
                        "Tag":0,
                        "Report":"Error no account"
                    }
                    send_client(accessed)
            # check service
            elif msg['CODE'] == ApplicationStates.CHECK_SERVICE.value:
                accessed =  {
                    "Tag": 0,
                    "Report":"Error"
                }
                if adr in account_tracker:
                    accessed =  {
                    "Tag": 2,
                    "Report":"Error"
                    }
                    #Get Service_ID
                    service_id = msg['FIR']
                    user_id = account_tracker[adr]
                    services_list = list_saved_services(user_id)
                    for service in services_list:
                        service = list(service)
                        if service_id == service[0]:
                            service_password = serverDecrypt(user_id,service_id)
                            accessed = {
                                "Tag":1,
                                "ServiceID":service_id,
                                "ServiceName": service[1],
                                "Username": service[2],
                                "Password": service_password
                            }
                            break
                    send_client(accessed)  
                else:
                    send_client(accessed)
            # Update Username and Password for a service
            elif msg['CODE'] == ApplicationStates.UPDATE_SERVICE.value:
                if adr in account_tracker:
                    service_id = msg['FIR']
                    new_service_name = msg['SEC']
                    new_service_username = msg['THR']
                    new_service_password = msg['FOR']
                    user_id = account_tracker[adr]
                    
                    services_list = list_saved_services(user_id)
                    accessed = {
                        'Tag':2
                    }
                    for service in services_list:
                        serv =list(service)
                        if service_id == serv[0]:
                            accessed = {
                                'Tag': 1,
                                'Name':0,
                                'User':0,
                                'Pass':0,
                            }
                            
                            if new_service_username != None: 
                                update_service_username(
                                    user_id, service_id, new_service_username)
                                accessed['User'] = 1
                                    
                            if new_service_password != None:
                                ciphertext, tag, cipher_key, mac_key = serverEncrypt(new_service_password)
                                update_service_password(
                                    user_id, service_id, ciphertext, tag, cipher_key, mac_key)
                                accessed['Pass'] = 1
                            
                            if new_service_name != None:
                                update_service_name(user_id, service_id,new_service_name)
                                accessed['name'] = 1
                            break   
                    send_client(accessed)   
                else:
                    accessed = {
                        "Tag":0,
                        "Report":"Error no account"
                    }
                    send_client(accessed)
            # Delete service
            elif msg['CODE'] == ApplicationStates.DELETE_SERVICE.value:
                if adr in account_tracker:
                    service_name = msg['FIR']
                    user_id = account_tracker[adr]
                    services_list = list_saved_services(user_id)
                    accessed = {
                        "Tag":0,
                        "Report":"Does not exist"
                    }
                    for name in services_list:
                        if name[0] == service_name:
                            accessed = {
                                "Tag":1,
                            }
                            delete_service(user_id, service_name)
                            break
                    send_client(accessed)
                else:
                    accessed = {
                        "Tag":0,
                        "Report":"Error no account"
                    }
                    send_client(accessed)
            # Delete account
            elif msg['CODE'] == ApplicationStates.DELETE_ACCOUNT.value:
                if adr in account_tracker:
                    user_id = account_tracker[adr]
                    delete_user(user_id)
                    accessed = {
                        "Tag":1
                    }
                else:
                    accessed = {
                        "Tag":0,
                        "Report":"Does not exist"
                    }
                send_client(accessed)
            elif msg['CODE'] == ApplicationStates.VERIFY.value:
                if adr in account_tracker:
                    store = list()
                    result = list_saved_services(account_tracker[adr])
                    for i in range (len(result)):
                        checker = list(result[i])
                        holder = serverDecrypt(account_tracker[adr],checker[0])
                        store.append([i,holder])
                    hold = list()
                    accessed = {
                        "Tag": 1
                    }
                    relist = list() #Holds if its a repeat
                    smallist = list()
                    for i in range(len(store)):
                        repeat = False
                        small = False
                        if store[i][1] in hold:
                            repeat = True
                            count = hold.index(store[i][1])
                            relist[count] = True
                        if len(store[i][1]) < 6:
                            small = True
                        hold.append(store[i][1])
                        relist.append(repeat)
                        smallist.append(small)
                    sending = list()
                    for i in range(len(hold)):
                        temp = list(result[i])
                        passed = str(temp[3])[2:-1]
                        if smallist[i] and relist[i]:
                            sending.append([temp[0],temp[1],temp[2],passed,True,True])
                        elif smallist[i]:
                            sending.append([temp[0],temp[1],temp[2],passed,True,False])
                        elif relist[i]:
                            sending.append([temp[0],temp[1],temp[2],passed,False,True])
                    holder = ''
                    hold.clear()
                    relist.clear()
                    smallist.clear()
                    result.clear()
                    accessed = {
                        "Tag": 1,
                        "Info": sending
                    }
                    send_client(accessed) 
                else:
                    accessed = {
                        "Tag":0,
                        "Report":"Does not exist"
                    }
                    send_client(accessed) 
            #Disconnect from server
            elif msg['CODE'] == ApplicationStates.DISCONNECT.value:
                if adr in account_tracker:
                    del account_tracker[adr]
                print(f"[{adr}] Has left the application")
                connected = False
                accessed = {
                    "Tag":1
                }
                send_client(accessed)            
            elif msg['CODE'] == ApplicationStates.LOGOFF.value:
                if adr in account_tracker:
                    del account_tracker[adr]
                    accessed = {
                        "Tag":1
                    }
                    send_client(accessed)
                else:
                    accessed = {
                        "Tag":0
                    }
                    send_client(accessed) 
    con.close()

if __name__ == "__main__":
    if not path.exists('passwords.db'):
        create_database()
        print('Database Created')
    server.listen()
    print(f"Connect to {SERVER}")
    while True:
        con, adr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con,adr))
        thread.start()
        print(f"[Accounts Connected] {threading.activeCount()-1}")