# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
if __name__ == '__main__':
    target = 'https://www.xbiquge6.com/81_81117/189469.html'
    server = 'https://www.xbiquge6.com'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    div_bf = BeautifulSoup(html)
    div = div_bf.find_all('div', id='content')
    print(div[0].text.replace('    ' , '\n'))