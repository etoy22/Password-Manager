import socket
import threading
import sqlite3
from os import path

from database_functions import (add_service, add_user, check_data_from_service, create_database,
                                delete_service, delete_user, get_master_pwd, get_key,
                                get_user_id, get_usernames_list, list_saved_services,
                                update_service_password, update_service_username)
from application_states import ApplicationStates

HEADER = 64
PORT = 3000
SERVER = socket.gethostbyname(socket.gethostname()) #Local Hosting
#SERVER =  # For connecting over internet put public adress ip
ADDRESS = (SERVER,PORT)
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

account_tracker = {SERVER:'HOST'}

def handle_client(con,adr):
    connected = True
    while connected:
        #decode message recived
        msg_length = con.recv(HEADER).decode(FORMAT)
        if msg_length:
            #Recive a message from client
            msg_length = int(msg_length)
            msg = con.recv(msg_length).decode(FORMAT).split("#")
            state = msg[0]
            # SIGN_UP 
            if int(state) == ApplicationStates.SIGN_UP.value:
                username = msg[1]
                password = msg[2]
                users_list = get_usernames_list()
                for name in users_list:
                    if username == name[0]:
                        #  user already exist
                        msgOut = "already exist".encode(FORMAT)
                        msgOut_length = len(msgOut)
                        send_length = str(msgOut_length).encode(FORMAT)
                        send_length += b' ' * (HEADER-len(send_length))
                        con.send(send_length)
                        con.send(msgOut)
                        return

                else:
                    try:
                        add_user(username, password)
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
            elif int(state) == ApplicationStates.LOGIN.value:
                #Change earlier than this so that it actually requires the username and passwords to be correct
                username = msg[1]
                password = msg[2]
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
            elif int(state) == ApplicationStates.GET_SERVICES.value:
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                senddata = ""
                for service in services_list:
                    senddata += service[0]+"#"
                senddata = senddata[:-1]
                msgOut = senddata.encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut)

            # in case add service
            elif int(state) == ApplicationStates.ADD_SERVICE.value:
                service_name = msg[1]
                service_username = msg[2]
                service_password = msg[3]                
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
                msgOut = accessed.encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut)
           
            # check service
            elif int(state) == ApplicationStates.CHECK_SERVICE.value:
                service_name = msg[1]
                user_id = account_tracker[adr[1]]
                services_list = list_saved_services(user_id)
                for service in services_list:
                    if service_name == service[0]:
                        service_username, service_password = check_data_from_service(user_id, service_name)
                        accessed = str(1)+"#"+service_username+"#"+service_password
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
            elif int(state) == ApplicationStates.UPDATE_SERVICE.value:
                service_name = msg[1]
                new_service_username = msg[2]
                new_service_password = msg[3]
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
            elif int(state) == ApplicationStates.DELETE_SERVICE.value:
                service_name = msg[1]
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
            elif int(state) == ApplicationStates.DELETE_ACCOUNT.value:
                user_id = account_tracker[adr[1]]
                delete_user(user_id)
            elif int(state) == ApplicationStates.DISCONNECT.value:
                del account_tracker[adr[1]]
                print(account_tracker)
                connected = False
            
    con.close()

if __name__ == "__main__":
    if not path.exists('passwords.db'):
        create_database()
    server.listen()
    print(f"{SERVER}")
    while True:
        con, adr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con,adr))
        thread.start()
        print(f"[Accounts Connected] {threading.activeCount()-1}")

        
  
    
