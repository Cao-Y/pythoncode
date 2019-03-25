# -*- coding:UTF-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
response = urlopen('http://www.chinanews.com/rss/scroll-news.xml')
res = BeautifulSoup(response.read(),"html.parser")

items =[] #结果数据
for item in res.find_all('item'):
    feed_item ={
        'title':item.title.text,
        'link':item.link.text,
        'desc':item.description.text,
        'pub_date':item.pubdate.text
    }

    items.append(feed_item)

with open('result.json','wt') as file:
    file.write(json.dumps(items))
#print(res)