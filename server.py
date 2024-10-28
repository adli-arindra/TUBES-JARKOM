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

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    server.sendall(send_len)
    server.sendall(message)

def start():
    server.listen()
    print(f"SERVER IS LISTENING ON {SERVER}")
    while True:
        conn, address = server.accept()
        print("\n", address)
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")

if __name__ == "__main__":
    print("SERVER IS STARTING...")
    threading.Thread(target=start).start()

    while True:
        msg = input("Enter your msg : ")
        send(msg)
        