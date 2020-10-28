from tcp_client import TCPClient
tcp_client = TCPClient('www.google.com')
print(tcp_client.request())
tcp_client.close()