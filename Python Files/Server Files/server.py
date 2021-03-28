'''
Note: This server was made using a tutoral on the subject. This tutorial helped to create the main and the handleClient
a link to the tutorial will be bellow
https://www.techwithtim.net/tutorials/socket-programming/
'''

import socket
import threading
import sqlite3
import json


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
    msgOut = message.encode(FORMAT)
    msgOut_length = len(msgOut)
    send_length = str(msgOut_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    con.send(send_length)
    con.send(msgOut)

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
                    if username == name[0]: #CHECK #11 - What is name[0]? is this an error
                        # user already exist
                        send_client("already exist")
                else: #CHECK #12 - Does this work?
                    try:
                        #CHECK #6 - Maybe we should make sure the password is secure
                        add_user(username, password)
                        account_tracker[adr]=username #Ethan added this for later parts
                        send_client("success")
                    except sqlite3.Error:
                        send_client("error")
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
                            #CHECK #13 - How are we getting the username? Maybe we could do account_tracker[adr]
                            user_id = get_user_id(username)
                            #CHECK #8 - What is adr[1]? adr refers to the computers adress
                            account_tracker[adr[1]] = user_id
                            #CHECK #7 - Make sure to make this number have a result when it sends back to the client
                            accessed = str(1)+"#"+str(user_id)
                            break
                        else:
                            #CHECK #14 - Make sure to make this number have a result when it sends back to the client
                            accessed = str(0)
                            break
                    else:
                        #CHECK #15 - Make sure to make this number have a result when it sends back to the client
                        accessed = str(2)
                    send_client(accessed)
            # send service list
            elif msg['CODE'] == ApplicationStates.GET_SERVICES.value:
                #CHECK #9 - Again what is adr[1]? Maybe replace with adr
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                senddata = ""
                #CHECK #1 - Might need to change how I data is sent back to the client
                for service in services_list:
                    senddata += service[0]+"#"
                senddata = senddata[:-1]
                send_client(senddata)
            # add service to account
            elif msg['CODE'] == ApplicationStates.ADD_SERVICE.value:
                service_name = msg['FIR']
                service_username = msg['SEC']
                service_password = msg['THR']
                #CHECK #16 - Adr[1] again? Same as earlier
                services_list = list_saved_services(account_tracker[adr[1]])
                for service in services_list:
                    if service_name == service[0]:
                        accessed = str(0)
                        return
                else:
                    #CHECK #17 - Adr[1] again? Same as earlier checks
                    user_id = account_tracker[adr[1]]
                    add_service(service_name, service_username,
                                service_password, user_id)
                    #CHECK #18 - Make sure this number has a response in client
                    accessed = str(1)
                #CHECK #2 - What is being sent here
                send_client(accessed)  
            # check service
            elif msg['CODE'] == ApplicationStates.CHECK_SERVICE.value:
                service_name = msg['FIR']
                #CHECK #19 - Adr[1] again? Same as earlier
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                for service in services_list:
                    if service_name == service[0]:
                        #CHECK #10 another case where we might need to change how data is sent
                        service_username, service_password = check_data_from_service(user_id, service_name)
                        #CHECK #20 - Change how this is sent back
                        accessed = str(1)+"#"+service_username+"#"+service_password
                        #CHECK #3 - Double check that this doesn't break out of loop 
                        break
                else:
                    #CHECK #21 - Make sure value has a response in client
                    accessed = str(0)
                send_client(accessed)  
            # Update Username and Password for a service
            elif msg['CODE'] == ApplicationStates.UPDATE_SERVICE.value:
                service_name = msg['FIR']
                new_service_username = msg['SEC']
                new_service_password = msg['THR']
                #CHECK #22 - Adr[1] again? Same as earlier
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                for name in services_list:
                    #CHECK #23 - What is name[0]? its not a length array
                    if name[0] == service_name:
                        service_exists = 1
                        if new_service_username == '':
                            update_service_password(user_id, service_name, new_service_password)
                        elif new_service_password == '':
                            update_service_username(user_id, service_name, new_service_username)
                        #CHECK #24 - I think this goes first as it has the most conditions
                        elif username != '' and password != '':
                            update_service_password(
                                user_id, service_name, new_service_password)
                            update_service_username(
                                user_id, service_name, new_service_username)
                            #CHECK #5 - make sure this doesn't break the code
                            break
                else:
                    #CHECK #25 - Make sure this has a value in client
                    service_exists = 0
                send_client(str(service_exists))   
            # Delete service
            elif msg['CODE'] == ApplicationStates.DELETE_SERVICE.value:
                service_name = msg['FIR']
                #CHECK #26 - Adr[1] again? Same as earlier
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                for name in services_list:
                    #CHECK #27 - Adr[1] name[0] again? Look at previous checks
                    if name[0] == service_name:
                        #CHECK #28 - Make sure this has value in client
                        service_exists = 1
                        delete_service(user_id, service_name)
                        break
                #CHECK #30 - does this even work
                else:
                    #CHECK #29 - Make sure this value has action in client
                    service_exists = 0
                send_client(str(service_exists))
            # Delete account
            elif msg['CODE'] == ApplicationStates.DELETE_ACCOUNT.value:
                #CHECK #4 - maybe require a username password verification
                #CHECK #31 - Adr[1] again? Same as earlier
                user_id = account_tracker[adr[1]]
                delete_user(user_id)
            #Disconnect from server
            elif msg['CODE'] == ApplicationStates.DISCONNECT.value:
                #CHECK #32 - Adr[1] again? Same as earlier
                if (adr[1]) in account_tracker:
                    del account_tracker[adr[1]]
                    #CHECK #33 - Delete later
                    print(account_tracker)
                print(f"[{adr}] Has left the application")
                connected = False
                send_client("Disconected")  
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