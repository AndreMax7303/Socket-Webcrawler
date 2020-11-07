import socket
import sys

from tcp_client import TCPClient
from bs4 import BeautifulSoup


img_suffix = ['.gif', '.jpeg', '.png', '.svg', '.webp', 'jpg']

# 1 - http://hostname/path/
# 2 - hostname/path/
# 3 - hostname/path/./img.png <- src = ./img.png -> hostname/img.png
# 4 - hostname/path/img.png <- src = img.png -> hostname/path/img.png
# 5 - hostname/path//img.png <- src = /img.png -> hostname/img.png
# 6 - hostname/path/./img.png <- src = /./img.png -> hostname/img.png


def get_path(url):
    if 'http://' in url:
        url = url[7:]
    url = url.split('/')
    del url[0]
    return '/'.join(url)


def get_hostname(url):
    if 'http://' in url:
        url = url[7:]
    url = url.split('/')
    hostname = url[0]
    return hostname


def treat_path(path):
    if path[0] != '/':
        return input_url + path
    else:
        tokens = path.split('/')
        try:
            pos = tokens.index('.')
            return get_hostname(input_url) + '/'.join(tokens[pos:])
        except ValueError:
            return get_hostname(input_url) + '/'.join(tokens)


def deal_with_text(response_body_bytes):
    beautiful_soup = BeautifulSoup(response_body_bytes.decode('utf8', 'replace'), 'html.parser')
    with open('index.html', 'w') as f:
        f.write(str(beautiful_soup))
    for img_element in beautiful_soup.findAll('img'):
        src = img_element.get('src')
        if 'http://' in src:
            request(src)
        else:
            request(treat_path(src))


def deal_with_img(img_bytes, filename):
    with open(filename, 'wb') as f:
        f.write(img_bytes)


def request(url):
    path = get_path(url)

    with TCPClient(get_hostname(url)) as tcp_client:
        response_body_bytes, content_type, status_code = tcp_client.request(path)
    if any(extension in path for extension in img_suffix):
        if status_code != 200:
            print('Falha no download da imagem')
            print('Status: ' + str(status_code))
            print('URL: ' + url)
            print('------------------------------')
            return
        deal_with_img(response_body_bytes, path.split('/')[-1])
    else:
        if status_code != 200:
            print('Falha no download do html base')
            print('Status: ' + str(status_code))
            print('!!! ENCERRANDO O PROGRAMA !!!')
            sys.exit(0)
        deal_with_text(response_body_bytes)





# 'www.ic.uff.br/~vefr/'
# 'http://www.ic.uff.br/index.php/pt/'
# input_url = 'http://www.ic.uff.br/index.php/pt/'
input_url = 'www.ic.uff.br/~vefr/'
request(input_url)

