import socket

from tcp_client import TCPClient
from bs4 import BeautifulSoup


def treat_url(url):
    if 'http://' in url:
        url = url.strip('http://')
    url = url.split('/')
    if '.' not in url[len(url)-1]:
        url[len(url)-1] += '/'
    hostname = url[0]
    del url[0]
    path = '/'.join(url)
    return hostname, path


def deal_with_text(response_body_bytes):
    beautiful_soup = BeautifulSoup(response_body_bytes.decode('utf8', 'replace'), 'html.parser')
    with open('index.html', 'w') as f:
        f.write(str(beautiful_soup))
    return beautiful_soup.findAll('img')


def deal_with_img(img_bytes, filename):
    with open(filename, 'wb') as f:
        f.write(img_bytes)


def request(url):
    hostname, path = treat_url(url)
    try:
        with TCPClient(hostname) as tcp_client:
            response_body_bytes, content_type, status_code = tcp_client.request(path)
            imgs = []
            if b'text' in content_type:
                if status_code != 200:
                    print('Status Code: ' + str(status_code))
                    print('!!!ENCERRANDO O PROGRAMA!!!')
                    return
                imgs = deal_with_text(response_body_bytes)
            for img_element in imgs:
                img_path = img_element.get('src')
                img_bytes, content_type, status_code = tcp_client.request(path + img_path)
                if status_code != 200:
                    print('Status Code: ' + str(status_code))
                    print('URL: ' + hostname + '/' + path + img_path)
                    continue
                deal_with_img(img_bytes, img_path.split('/')[-1])
    except socket.gaierror:
        print("Esse hostname é inválido")
        print('!!!ENCERRANDO O PROGRAMA!!!')
    except:
        print("Erro desconhecido")



# 'www.ic.uff.br/~vefr/'
# 'www2.ic.uff.br/~anselmo/'
# 'www.ic.uff.br/~aconci'
request('www.ic.uff.br/~vefr/icons/MarbleLine.gif')

