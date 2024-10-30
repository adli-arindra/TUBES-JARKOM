import socket
import threading
from const import *

class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(self.socket)
        self.message = ""
        self.sender = ""

    def connect(self) -> bool:
        try:
            self.send(SYN)
            response = self.recv()
            if (response == SYN_ACK):
                return True
            else:
                raise Exception()
        except:
            return False

    def validate(self, content) -> bool:
        self.send(content)
        respond = self.recv()
        if respond == TRUE:
            return True
        else:
            return False

    def send(self, msg:str) -> None:
        self.socket.sendto(msg.encode(FORMAT), SERVER)
    
    def recv(self) -> str:
        msg, address = self.socket.recvfrom(1024)
        msg = msg.decode(FORMAT)
        print(msg)
        return msg
    
    def startListening(self):
        threading.Thread(target=self.listen).start()

    def listen(self) -> None:
        print("Joined chatroom")
        while True:
            raw_msg = self.recv()
            username, msg = raw_msg.split(':')
            self.message = msg
            self.sender = username



# client = Client()