import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISC"
SERVER = "192.168.56.1"
ADDRESS = (SERVER, PORT)

target = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def listen():
    connected = True
    while connected:
        msg_length = int(client.recv(HEADER).decode(FORMAT))
        msg = client.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
    
        print(msg)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

if __name__ == "__main__":
    target = client.getsockname()[0] + "-" + str(client.getsockname()[1])
    listening = threading.Thread(target=listen)
    listening.start()

    print("<IP Address>-<PORT>:<MSG>")
    while True:
        msg = input("> ")
        try:
            if ('-' in msg):
                target = msg.split(':')[0]
                msg = msg.split(':')[1]
            send(target + ':' + msg)
        except:
            print("Pesan gagal dikirim!")