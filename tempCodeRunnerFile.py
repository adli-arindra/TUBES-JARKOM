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