from tcp_client import TCPClient
from bs4 import BeautifulSoup


def split_url(url):
    url = url.split('/')
    hostname = url[0]
    del url[0]
    path = ''.join(url)
    return hostname, path


def request(url):
    hostname, path = split_url(url)
    with TCPClient(hostname) as tcp_client:
        response = tcp_client.request(path)
        status_code = int(response[9:12])
        print(status_code)
        # print(response)



# 'www.ic.uff.br/~vefr/'
request('www.ic.uff.br/~vefr/')
# soup = BeautifulSoup(tcp_client.request(), 'html.parser')
