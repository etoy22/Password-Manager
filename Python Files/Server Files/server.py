'''
Note: This server was made using a tutoral on the subject. This tutorial helped to create the main and the handleClient
a link to the tutorial will be bellow
https://www.techwithtim.net/tutorials/socket-programming/
'''

import socket
import threading
import sqlite3
import json
import encrypt

from os import path

from database_functions import (add_service, add_user, check_data_from_service, create_database,
                                delete_service, delete_user, get_master_pwd, get_key,
                                get_user_id, get_usernames_list, list_saved_services,
                                update_service_password, update_service_username)

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

def serverEncrypt(service_username,service_password,adr):
    '''
    
    '''
    accountUsername = get_username(account_tracker[adr])
    accountPassword = get_master_pwd(accountUsername)
    return ciphertext, tag = encrypt.encrypt_then_mac(service_password,masterPassword,service_username,accountUsername)

def serverDecrypt(user_id,service_name,adr):
    '''
    check_data_from_service needs to give tag as well
    '''
    service_username, ciphertext = check_data_from_service(user_id, service_name)
    tag =""
    service_password = encrypt.verify_then_decrypt(ciphertext,tag,service_username,account_tracker[adr])
    return service_password

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
                        "Tag":0,
                        "Report":"Already exist"
                    }
                    send_client(accessed)
                
            #Case if someone attempts to login
            elif msg['CODE'] == ApplicationStates.LOGIN.value:
                #Change earlier than this so that it actually requires the username and passwords to be correct
                username = msg['FIR']
                password = msg['SEC']
                #  Checking if user exists
                users_list = get_usernames_list()
                #CHECK #34 - Make sure this number has a result
                accessed = {
                    "Tag":0,
                    "Report":"Issue with username or password"
                } #The username or password has an issue
                for user in users_list:
                    if username == user[0]:
                        if password == get_master_pwd(username):
                            user_id = get_user_id(username)
                            account_tracker[adr] = user_id
                            #CHECK #36 - What is this suppose to send 
                            accessed = {
                                "Tag":1,
                                "User_id":user_id
                            }
                            break
                send_client(accessed)
            # send service list
            elif msg['CODE'] == ApplicationStates.GET_SERVICES.value:
                if adr in account_tracker:
                    user_id = account_tracker[adr]
                    services_list = list_saved_services(user_id)
                    #CHECK #1 - Might need to change how I data is sent back to the client
                    accessed = {
                        "Tag":1
                    }
                    i = 0
                    for service in services_list:
                        accessed[("sendData"+i)] = service[0]
                        
                    '''
                    Did i mess this up
                    '''
                    # senddata = senddata[:-1]
                    
                    # senddata = ""
                    # #CHECK #1 - Might need to change how I data is sent back to the client
                    # for service in services_list:
                    #     senddata += service[0]+"#"
                    # senddata = senddata[:-1]
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
                    flip = True
                    for service in services_list:
                        if service_name == service[0]:
                            #CHECK #38 - update for service_id
                            accessed = {
                                "Tag":0,
                                "Report":"Same Service"
                            }
                            flip = False
                            break
                    if flip:
                        user_id = account_tracker[adr]
                        ciphertext, tag = serverEncrypt(service_username,service_password,service_id,adr)
                        #ASDF
                        '''
                        Add tag to add_service
                        '''
                        add_service(service_name, service_username,
                                    ciphertext, user_id)
                        #CHECK #18 - Make sure this number has a response in client
                        accessed = {
                            "Tag":1
                        }                    
                        #CHECK #2 - What is being sent here
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
                    service_name = msg['FIR']
                    user_id = account_tracker[adr]
                    services_list = list_saved_services(user_id)
                    
                    for service in services_list:
                        if service_name == service:
                            service_password = serverDecrypt(user_id,service_name,adr)
                            accessed = {
                                "Tag":1,
                                "Username": service_username,
                                "Password": service_password
                            }
                            break
                    send_client(accessed)  
                else:
                    send_client(accessed)
            # Update Username and Password for a service
            elif msg['CODE'] == ApplicationStates.UPDATE_SERVICE.value:
                if adr in account_tracker:
                    service_name = msg['FIR']
                    new_service_username = msg['SEC']
                    new_service_password = msg['THR']
                    user_id = account_tracker[adr]
                    services_list = list_saved_services(user_id)
                    flip = True
                    for name in services_list:
                        if name == service_name:
                            flip = False
                            if new_service_username != None and new_service_password != None:
                                new_service_password, tag = serverEncrypt(new_service_name,service_password,adr)
                                '''
                                Add tag to update_service_password
                                '''
                                update_service_password(
                                    user_id, service_name, new_service_password)
                                update_service_username(
                                    user_id, service_name, new_service_username)
                                break
                            elif new_service_username == None:
                                '''
                                Add tag
                                '''
                                new_service_password,tag = serverEncrypt(service_name,service_password,adr)
                                update_service_password(user_id, service_name, new_service_password)
                                break
                            elif new_service_password == None:
                                update_service_username(user_id, service_name, new_service_username)
                                break
                            accessed = {
                                "Tag":1
                            }
                    if flip:
                        #CHECK #25 - Make sure this has a value in client
                        accessed = {
                            "Tag":0,
                            "Report":"Service does not exist"
                        }                    
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
                    #CHECK #29 - Make sure this value has action in client
                    accessed = {
                        "Tag":0,
                        "Report":"Does not exist"
                    }
                    for name in services_list:
                        if name[0] == service_name:
                            #CHECK #28 - Make sure this has value in client
                            accessed = {
                                "Tag":1,
                                "Report":"Does not exist"
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
                #CHECK #4 - maybe require a username password verification
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
            #Disconnect from server
            elif msg['CODE'] == ApplicationStates.DISCONNECT.value:
                if adr in account_tracker:
                    del account_tracker[adr]
                print(f"[{adr}] Has left the application")
                connected = False
                accessed = {
                    "Tag":"1"
                }
                send_client(accessed)
    con.close()

if __name__ == "__main__":
    if not path.exists('passwords.db'):
        create_database()
    server.listen()
    print(f"Connect to {SERVER}")
    while True:
        con, adr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con,adr))
        thread.start()
        print(f"[Accounts Connected] {threading.activeCount()-1}")