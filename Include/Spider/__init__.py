# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests,sys
class downloader(object):
    def __init__(self):
        self.server = 'https://www.xbiquge6.com/'
        self.target = 'https://www.xbiquge6.com/81_81117/'
        self.names = []
        self.urls = []
        self.nums = 0

    def get_download_url(self):
        req = requests.get(url=self.target)
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', id='list')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, target):
        req = requests.get(url=target)
        req.encoding = 'utf-8'
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', id='content')
        texts = div[0].text.replace('    ', '\n')
        return texts

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + 'n')
            f.writelines(text)
            f.write('nn')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《仙尊》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '仙尊.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" % float(i / dl.nums) + 'r')
        sys.stdout.flush()
        print('《仙尊》下载完成')






# if __name__ == '__main__':
#     target = 'https://www.xbiquge6.com/81_81117/'
#     server = 'https://www.xbiquge6.com'
#     req = requests.get(url=target)
#     req.encoding = 'utf-8'
#     html = req.text
#     div_bf = BeautifulSoup(html)
#     div = div_bf.find_all('div', id = 'list')
#     a_bf = BeautifulSoup(str(div[0]))
#     a = a_bf.find_all('a')
#     for each in a:
#         print(each.string, server + each.get('href'))