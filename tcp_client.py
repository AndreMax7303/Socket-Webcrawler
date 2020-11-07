import socket


def get_content(search, response):
    found = next((s for s in response if search in s), None)
    if found:
        length = found.split(b' ')[1]
        return True, length
    else:
        return False, 0


def get_status(token):
    return int(token.split()[1])


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
        has_content_type, content_type = get_content(b'Content-Type', received_split)
        if not has_content_type:
            content_type = 'text/plain'
        is_content_length, content_length = get_content(b'Content-Length', received_split)
        if is_content_length:
            while len(received) < int(content_length):
                received += self.socket.recv(self.buffsize)
        status_code = get_status(received_split[0])
        return received, content_type, status_code

    def __exit__(self, type, value, tb):
        self.socket.close()
