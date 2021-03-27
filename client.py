import socket
import sys

sys.path.append('./Pages')
sys.path.append('./Pages/Helper_Functions')
import GeneratorPage as genPage

HEADER = 64
PORT = 3000
FORMAT = 'utf-8'
DISCONECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = # For connecting over internet put public adress ip
ADDRESS = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)


def send (msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    # msg_length = client.recv(HEADER).decode(FORMAT)
    # if msg_length:
    #     msg_length = int(msg_length)
    #     msg = client.recv(msg_length).decode(FORMAT)
    #     print(msg)

if __name__ == "__main__":
    genPage.screen()
    send(DISCONECT_MESSAGE)
