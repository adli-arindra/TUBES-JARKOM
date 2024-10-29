import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISC"
SERVER_PASS = "jarkomjuara"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

clients = {}
usernames = {}

def start():
    server.listen()
    print(f"SERVER IS LISTENING ON {SERVER}")
    while True:
        conn, address = server.accept()
        index = address[0] + "-" + str(address[1])
        clients[index] = conn
        thread = threading.Thread(target=handle_client, args=(conn, index))
        thread.start()

def validateUsername(conn, index) -> bool:
    uname_length = int(conn.recv(HEADER).decode(FORMAT))
    uname = conn.recv(uname_length).decode(FORMAT)
    print(uname)
    if uname in usernames.values():
        forward(index, index + ":0")
        return True
    else:
        usernames[index] = uname
        forward(index, index + ":1")
        return False

def validatePassword(conn, index) -> bool:
    pass_length = int(conn.recv(HEADER).decode(FORMAT))
    password = conn.recv(pass_length).decode(FORMAT)
    if password == (SERVER_PASS):
        forward(index, index + ":1")
        return True
    else:
        forward(index, index + ":0")
        return False

def handle_client(conn, index):
    print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")
    if not validatePassword(conn, index): return
    if not validateUsername(conn, index): return
    connected = True
    while connected:
        msg_length = int(conn.recv(HEADER).decode(FORMAT))
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
    
        forward(index, msg)

    conn.close()

def forward(index, msg):
    targetIndex = msg.split(':')[0]
    msg = f"[{index}] : " + msg.split(':')[1]
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    clients[targetIndex].send(send_len)
    clients[targetIndex].send(message)


if __name__ == "__main__":
    start()