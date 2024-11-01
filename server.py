import socket
import threading
from const import *
from time import sleep
from caesarcipher import encrypt, decrypt

class Server():
    clients = {}
    last_msg = ""
    last_addr = ""

    def __init__(self):
        print(f"STARTING SERVER [{SERVER_IP}, {PORT}]")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((SERVER_IP, PORT))

        while True:
            self.last_msg, self.last_addr = self.recv()
            if self.last_msg == SYN:
                threading.Thread(target=self.handleClient, kwargs={'address':self.last_addr}).start()
    
    def send(self, msg, address) -> None:
        msg = encrypt(msg)
        self.socket.sendto(msg.encode(FORMAT), address)
        self.last_msg = ""
        self.last_addr = ""

    def sendToAll(self, msg) -> None:
        for i in self.clients.values():
            self.send(msg, i)

    def recv(self) -> tuple:
        msg, address = self.socket.recvfrom(1024)
        msg = msg.decode(FORMAT)
        msg = decrypt(msg)
        print(msg)
        return (msg, address)

    def handleClient(self, address) -> bool:
        self.send(SYN_ACK, address)
        connected = True
        password_valid = self.validatePassword(address)
        if not password_valid: return False
        username_valid = self.validateUsername(address)
        if not username_valid: return False

        print("CONNECTED TO ", address)

        while connected:
            sleep(0.1)
            if self.last_addr == address:
                username = ""
                for k, v in self.clients.items():
                    if v == address:
                        username = k
                        break
                if "-" in self.last_msg:
                    target_ip = self.last_msg.split("-")[0]
                    target_port = int(self.last_msg.split("-")[1])
                    msg = username + ":" + "<private-msg> " + self.last_msg.split("-")[2]
                    self.send(msg, (target_ip, target_port))
                else:
                    msg = username + ":" + self.last_msg
                    self.sendToAll(msg)

    def validatePassword(self, address) -> bool:
        while self.last_addr != address:
            sleep(0.1)
        else:
            if self.last_msg == SERVER_PASS:
                self.send(TRUE, address)
                return True
            else:
                self.send(FALSE, address)
                return False
    
    def validateUsername(self, address) -> bool:
        while self.last_addr != address:
            sleep(0.1)
        else:
            if not self.last_msg in self.clients:
                self.clients[self.last_msg] = self.last_addr
                self.send(TRUE, address)
                return True
            else:
                self.send(FALSE, address)
                return False
    


if __name__ == "__main__":
    server = Server()