import socket

class TCPClient:
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, 80))

    def request(self):
        self.socket.send('GET / HTTP/1.1\r\n\r\n'.encode('UTF-8'))
        return self.socket.recv(4096)

    def close(self):
        self.socket.close()