# -*- coding:UTF-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
response = urlopen('http://www.chinanews.com/rss/rss_2.html')
res = BeautifulSoup(response.read(),"html.parser")
rss_links = set([item['href']for item in res.find_all('a')])

def crawl_feed(url):
    response =urlopen(url)
    rss = BeautifulSoup(response.read(),"lxml")
    items = []
    print("Crawling %s" %url)

    for item in rss.find_all('item'):
        try:
            feed_item = {
                'title': item.title.text,
                'link': item.contents[2],
                'desc': item.description.text,
                'pub_date':u''if item.pubdate is None else item.pubdate.text
            }
            items.append(feed_item)
        except Exception as e:
            print('Crawling %s error.' %url)
            print(e)
    return items

feed_items =[]

for link in rss_links:
    feed_items += crawl_feed(link)

print(feed_items)  #输出内容

with open('result.json','w') as file:  #写入json文件
    file.write(json.dumps(feed_items))

print('Total crawl %s items ' %len(feed_items))    #输出内容长度






# items =[] #结果数据
# for item in res.find_all('item'):
#     feed_item ={
#         'title':item.title.text,
#         'link':item.link.text,
#         'desc':item.description.text,
#         'pub_date':item.pubdate.text
#     }
#
#     items.append(feed_item)
#
# with open('result.json','wt') as file:
#     file.write(json.dumps(items))
#print(res)