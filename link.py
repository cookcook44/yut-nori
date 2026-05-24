from socket import socket, AF_INET, SOCK_DGRAM
sock = socket(AF_INET, SOCK_DGRAM)


class Link:
    def __init__(self):
        self.my_addr = ("_", -1)
        self.opp_addr = ("_", -1)
        self.first_link = 0
    def account(self):
        from utils import _utils
        self.first_link = 1
        try:
            self.my_addr = ("127.0.0.1", 8000)
            self.opp_addr = ("127.0.0.1", 8001)
            sock.bind(self.my_addr)
            _utils.user = 1
            print("1p임") # 1회한정 프린트
        except OSError:
            self.my_addr = ("127.0.0.1", 8001)
            self.opp_addr = ("127.0.0.1", 8000)
            sock.bind(self.my_addr)
            _utils.user = 2
            print("2p임") # 1회한정 프린트

_link = Link()