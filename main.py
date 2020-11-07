from tcp_client import TCPClient
from bs4 import BeautifulSoup
from enum import Enum

class DownloadType(Enum):
    TXT = 1
    IMG = 2


def split_url(url):
    url = url.split('/')
    if '.' not in url[len(url)-1]:
        url[len(url)-1] += '/'
    hostname = url[0]
    del url[0]
    path = '/'.join(url)
    return hostname, path


def request(url, download_type):
    hostname, path = split_url(url)
    with TCPClient(hostname) as tcp_client:
        response = tcp_client.request(path)
        status_code = int(response[9:12])
        # if status_code != 200:
        #     print('Status: {}'.format(status_code))
        #     if download_type == DownloadType.TXT:
        #         print('!!!Exiting program!!!')
        #         return
        #     else:
        #         print('URL: {}'.format(url))
        #         return
        print(status_code)
        print(response)



# 'www.ic.uff.br/~vefr/'
request('www.ic.uff.br/~vefr', DownloadType.IMG)
# soup = BeautifulSoup(tcp_client.request(), 'html.parser')
