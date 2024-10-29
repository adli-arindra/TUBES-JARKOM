import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISC"
SERVER = "192.168.56.1"
ADDRESS = (SERVER, PORT)

target = ""

def listen():
    connected = True
    while connected:
        msg_length = int(client.recv(HEADER).decode(FORMAT))
        msg = client.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
    
        print(msg)
        print("> ")

def send(client, target, msg):
    message = target + ':' + msg
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

def connect():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.connect(ADDRESS)
        index = client.getsockname()[0] + "-" + str(client.getsockname()[1])
        return (client, index)
    except:
        return False

def validateUsername(client, selfIndex, username) -> bool:
    send(client, selfIndex, username)
    print(username)
    msg_length = int(client.recv(HEADER).decode(FORMAT))
    msg:str = client.recv(msg_length).decode(FORMAT)
    print(msg)
    if msg.endswith('1'):
        return True
    else:
        return False

def validatePassword(client, selfIndex, password):
    send(client, selfIndex, password)
    msg_length = int(client.recv(HEADER).decode(FORMAT))
    msg = client.recv(msg_length).decode(FORMAT)
    if msg.endswith('1'):
        return True
    else:
        return False


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

    target = client.getsockname()[0] + "-" + str(client.getsockname()[1])
    print(target)
    listening = threading.Thread(target=listen)
    listening.start()

    connected = False

    print("<IP Address>-<PORT>:<MSG>")
    while True:
        msg = input("> ")
        try:
            if (':' in msg):
                target = msg.split(':')[0]
                msg = msg.split(':')[1]
            send(target + ':' + msg)
        except:
            print("Pesan gagal dikirim!")