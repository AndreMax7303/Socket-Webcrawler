import socket


def get_msg_length(response):
    found = next((s for s in response if b'Content-Length' in s), None)
    if found:
        length = int(found.split(b' ')[1])
        return True, length
    else:
        return False, 0


class TCPClient:
    def __init__(self, hostname):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.hostname = hostname
        self.buffsize = 4096

    def __enter__(self):
        self.socket.connect((self.hostname, 80))
        return self

    def request(self, path):
        print(path)
        self.socket.send('GET /{} HTTP/1.1 \r\nHost: {} \r\nAccept-Encoding: identity \r\n\r\n'.format(path, self.hostname).encode('UTF-8'))
        received = self.socket.recv(self.buffsize)
        received_split = received.split(b'\r\n\r\n')[0].split(b'\r\n')
        is_content_length, content_length = get_msg_length(received_split)
        if is_content_length:
            while len(received) < content_length:
                received += self.socket.recv(self.buffsize)
        return received

    def __exit__(self, type, value, tb):
        self.socket.close()
