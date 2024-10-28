import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISC"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

clients = {}

def start():
    server.listen()
    print(f"SERVER IS LISTENING ON {SERVER}")
    while True:
        conn, address = server.accept()
        index = address[0] + "-" + str(address[1])
        clients[index] = conn
        print(clients[index])
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()


def handle_client(conn, addr):
    print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")
    connected = True
    while connected:
        msg_length = int(conn.recv(HEADER).decode(FORMAT))
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
    
        # print(f"[{addr}] : {msg}")
        forward(addr, msg)

    conn.close()

def forward(addr, msg):
    index = msg.split(':')[0]
    msg = f"[{addr}] : " + msg.split(':')[1]
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    clients[index].send(send_len)
    clients[index].send(message)


if __name__ == "__main__":
    start()