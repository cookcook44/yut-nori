from socket import socket, AF_INET, SOCK_DGRAM
BUF_SIZE = 1024
sock = socket(AF_INET, SOCK_DGRAM)

import utils as utils

class Link:
    def __init__(self):
        self.my_addr = ("_", -1)
        self.opp_addr = ("_", -1)
        self.first_link = 0
    def account(self):
        self.first_link = 1
        try:
            self.my_addr = ("127.0.0.1", 8000)
            self.opp_addr = ("127.0.0.1", 8001)
            sock.bind(self.my_addr)
            utils.user = 1
        except OSError:
            self.my_addr = ("127.0.0.1", 8001)
            self.opp_addr = ("127.0.0.1", 8000)
            sock.bind(self.my_addr)
            utils.user = 2