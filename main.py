import socket

from tcp_client import TCPClient
from bs4 import BeautifulSoup


def treat_url(url):
    if 'http://' in url:
        url = url[7:]
    url = url.split('/')
    hostname = url[0]
    del url[0]
    path = '/'.join(url)
    return hostname, path


def deal_with_text(response_body_bytes):
    beautiful_soup = BeautifulSoup(response_body_bytes.decode('utf8', 'replace'), 'html.parser')
    with open('index.html', 'w') as f:
        f.write(str(beautiful_soup))
    for img_element in beautiful_soup.findAll('img'):
        src = img_element.get('src')
        if 'http://' in src:
            request(src)
        else:
            request(input_url + img_element.get('src'))


def deal_with_img(img_bytes, filename):
    with open(filename, 'wb') as f:
        f.write(img_bytes)


def request(url):
    hostname, path = treat_url(url)
    try:
        with TCPClient(hostname) as tcp_client:
            response_body_bytes, content_type, status_code = tcp_client.request(path)
        if b'text' in content_type:
            if status_code != 200:
                print('Status: ' + str(status_code))
                print('!!! ENCERRANDO O PROGRAMA !!!')
                exit(-1)
            deal_with_text(response_body_bytes)
        else:
            if status_code != 200:
                print('Status: ' + str(status_code))
                print('URL: ' + url)
                print('------------------------------')
                return
            deal_with_img(response_body_bytes, path.split('/')[-1])
    except socket.gaierror:
        print("Esse hostname é inválido")
        print('!!!ENCERRANDO O PROGRAMA!!!')
    except:
        print("Erro desconhecido")



# 'www.ic.uff.br/~vefr/'
input_url = 'www.ic.uff.br/~vefr/'
request(input_url)

