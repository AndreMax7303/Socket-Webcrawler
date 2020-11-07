from tcp_client import TCPClient
from bs4 import BeautifulSoup
from enum import Enum


def split_url(url):
    url = url.split('/')
    if '.' not in url[len(url)-1]:
        url[len(url)-1] += '/'
    hostname = url[0]
    del url[0]
    path = '/'.join(url)
    return hostname, path


def request(url):
    hostname, path = split_url(url)
    with TCPClient(hostname) as tcp_client:
        response, content_type, status_code = tcp_client.request(path)

        print(response)



# 'www.ic.uff.br/~vefr/'
request('www.ic.uff.br/~vefr')
# soup = BeautifulSoup(tcp_client.request(), 'html.parser')
