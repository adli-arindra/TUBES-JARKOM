import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISC"
SERVER = "192.168.56.1"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)



def handle_client(conn, addr):
    print(f"NEW CONNECTION: {addr}\n")

    connected = True
    while connected:
        msg_length = int(conn.recv(HEADER).decode(FORMAT))
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
    
        print(f"[{addr}] : {msg}")

    conn.close()

if __name__ == "__main__":
    listen = threading.Thread(target=handle_client, args=(client, ADDRESS))
    listen.start()

    while True:
        msg = input()
        send(msg)