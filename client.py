import socket
import threading
from const import *

class Client():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

    def send(self, msg) -> None:
        self.socket.sendto(msg.encode(FORMAT), SERVER)
        print(">", msg)
    
    def recv(self) -> str:
        msg, address = self.socket.recvfrom(1024)
        msg = msg.decode(FORMAT)
        return msg


client = Client()