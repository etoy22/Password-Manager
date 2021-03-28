'''
Note: This server was made using a tutoral on the subject. This tutorial helped to create the main and the handleClient
a link to the tutorial will be bellow
https://www.techwithtim.net/tutorials/socket-programming/
'''

import socket
import threading
import sqlite3
import sys
import json

sys.path.append('./')
sys.path.append('./Pages')
sys.path.append('./Pages/Helper_Functions')

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

#Currently Contains IP to give current user name
account_tracker = {SERVER:'HOST'}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def send_client(message):
    msgOut = message.encode(FORMAT)
    msgOut_length = len(msgOut)
    send_length = str(msgOut_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    return msgOut,send_length


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
                for name in users_list:
                    if username == name[0]:
                        #  user already exist
                        msgOut, send_length = send_client("already exist")
                        con.send(send_length)
                        con.send(msgOut)
                    else:
                        try:
                            #CHECK #6 - Maybe we should make sure the password is secure
                            add_user(username, password)
                            account_tracker[adr]=username
                            msgOut = "success".encode(FORMAT)
                            msgOut_length = len(msgOut)
                            send_length = str(msgOut_length).encode(FORMAT)
                            send_length += b' ' * (HEADER-len(send_length))
                            con.send(send_length)
                            con.send(msgOut)
                        except sqlite3.Error:
                            msgOut = "error".encode(FORMAT)
                            msgOut_length = len(msgOut)
                            send_length = str(msgOut_length).encode(FORMAT)
                            send_length += b' ' * (HEADER-len(send_length))
                            con.send(send_length)
                            con.send(msgOut)      
            #Case if someone attempts to login
            elif msg['CODE'] == ApplicationStates.LOGIN.value:
                #Change earlier than this so that it actually requires the username and passwords to be correct
                username = msg['FIR']
                password = msg['SEC']
                #  Checking if user exists
                users_list = get_usernames_list()

                for user in users_list:
                    if username == user[0]:
                        if password == get_master_pwd(username):
                            user_id = get_user_id(username)
                            account_tracker[adr[1]] = user_id
                            accessed = str(1)+"#"+str(user_id)
                            break
                        else:
                            accessed = str(0)
                            break
                    else:
                        accessed = str(2)
                    msgOut = accessed.encode(FORMAT)
                    msgOut_length = len(msgOut)
                    send_length = str(msgOut_length).encode(FORMAT)
                    send_length += b' ' * (HEADER-len(send_length))
                    con.send(send_length)
                    con.send(msgOut)
            # send service list
            elif msg['CODE'] == ApplicationStates.GET_SERVICES.value:
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                senddata = ""
                for service in services_list:
                    senddata += service[0]+"#"
                senddata = senddata[:-1]
                #CHECK 1
                msgOut = senddata.encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut)
            # add service to account
            elif msg['CODE'] == ApplicationStates.ADD_SERVICE.value:
                service_name = msg['FIR']
                service_username = msg['SEC']
                service_password = msg['THR']                
                services_list = list_saved_services(account_tracker[adr[1]])
                for service in services_list:
                    if service_name == service[0]:
                        accessed = str(0)
                        return
                else:
                    user_id = account_tracker[adr[1]]
                    add_service(service_name, service_username,
                                service_password, user_id)
                    accessed = str(1)
                #CHECK 2 - What is being sent here
                msgOut = accessed.encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut)     
            # check service
            elif msg['CODE'] == ApplicationStates.CHECK_SERVICE.value:
                service_name = msg['FIR']
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                for service in services_list:
                    if service_name == service[0]:
                        service_username, service_password = check_data_from_service(user_id, service_name)
                        accessed = str(1)+"#"+service_username+"#"+service_password
                        #CHECK 3 - Double check that this doesn't break out of loop 
                        break
                else:
                    accessed = str(0)
                msgOut = accessed.encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut)
             # Update service
            # Update Username and Password for a service
            elif msg['CODE'] == ApplicationStates.UPDATE_SERVICE.value:
                service_name = msg['FIR']
                new_service_username = msg['SEC']
                new_service_password = msg['THR']
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                for name in services_list:
                    if name[0] == service_name:
                        service_exists = 1
                        if new_service_username == '':
                            update_service_password(user_id, service_name, new_service_password)
                        elif new_service_password == '':
                            update_service_username(user_id, service_name, new_service_username)
                        elif username != '' and password != '':
                            update_service_password(
                                user_id, service_name, new_service_password)
                            update_service_username(
                                user_id, service_name, new_service_username)
                            #CHECK 5 - make sure this doesn't break the code
                            break
                else:
                    service_exists = 0
                msgOut = str(service_exists).encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut)
            # Delete service
            elif msg['CODE'] == ApplicationStates.DELETE_SERVICE.value:
                service_name = msg['FIR']
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                for name in services_list:
                    if name[0] == service_name:
                        service_exists = 1
                        delete_service(user_id, service_name)
                        break
                else:
                    service_exists = 0
                msgOut = str(service_exists).encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut) 
            # Delete account
            elif msg['CODE'] == ApplicationStates.DELETE_ACCOUNT.value:
                #CHECK 4 - maybe require a username password verification from server
                user_id = account_tracker[adr[1]]
                delete_user(user_id)
            #Disconnect from server
            elif msg['CODE'] == ApplicationStates.DISCONNECT.value:
                if (adr[1]) in account_tracker :
                    del account_tracker[adr[1]]
                    print(account_tracker)
                print(f"[{adr}] Has left the application")
                connected = False
    con.close()

if __name__ == "__main__":
    server.listen()
    print(f"Connect to {SERVER}")
    while True:
        con, adr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con,adr))
        thread.start()
        print(f"[Accounts Connected] {threading.activeCount()-1}")

        
  
    
