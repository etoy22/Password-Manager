import socket
import threading


HEADER = 64
PORT = 3000
SERVER = socket.gethostbyname(socket.gethostname()) #Local Hosting
#SERVER =  # For connecting over internet put public adress ip
ADDRESS = (SERVER,PORT)
COLLECT = ""
FORMAT = 'utf-8'

#Codes
DISCONECT_MESSAGE = "DISCONNECT"
LOGIN = "LOG"
COLLECT = ""

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
            msg = con.recv(msg_length).decode(FORMAT)
            #Disconnect message from client to server
            if msg == DISCONECT_MESSAGE:
                del account_tracker[adr]
                print(account_tracker)
                connected = False
            #Case if someone attempts to login
            elif msg == LOGIN:
                #Change earlier than this so that it actually requires the username and passwords to be correct
                if True:
                    account_tracker[adr] = 'Jack'
                    print(account_tracker)
                msgOut = "Login attempt".encode(FORMAT)
                msgOut_length = len(msgOut)
                send_length = str(msgOut_length).encode(FORMAT)
                send_length += b' ' * (HEADER-len(send_length))
                con.send(send_length)
                con.send(msgOut)
  
            # elif msg == COLLECT:       
            #     pass
            #Send message from server to client
            
    con.close()

if __name__ == "__main__":
    server.listen()
    print(f"{SERVER}")
    while True:
        con, adr = server.accept()
        thread = threading.Thread(target=handle_client, args=(con,adr))
        thread.start()
        print(f"[Accounts Connected] {threading.activeCount()-1}")

        
  
    
