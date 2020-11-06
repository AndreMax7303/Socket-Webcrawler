import socket


class TCPClient:
    def __init__(self, hostname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostname = hostname
        self.buffsize = 4096

    def __enter__(self):
        self.socket.connect((self.hostname, 80))
        return self

    def request(self, path):
        self.socket.send('GET /{}/ HTTP/1.1 \r\nHost: {} \r\n\r\n'.format(path, self.hostname).encode('UTF-8'))
        result = ''
        while True:
            received = self.socket.recv(self.buffsize).decode('UTF-8', 'replace')
            result += received
            if len(received) < self.buffsize:
                break
        return result

    def __exit__(self, type, value, tb):
        self.socket.close()
