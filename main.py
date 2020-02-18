import re
import json
try:
	import requests
	from lxml.html import etree
except ImportError:
	import os
	os.system('pip install requests')
	os.system('pip install lxml')
	import requests
	from lxml.html import etree

# 网站根目录
root = 'http://www.xiachufang.com'

# headers可以多一点伪装
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'}

# 抓取本周最热1000道菜url链接
detail_list = list()
for i in range(1,40+1):
    url = 'http://www.xiachufang.com/explore/?page=%d' % i
    rsp = requests.get(url=url,headers=headers)
    html = etree.HTML(rsp.text)
    detail_list.extend(html.xpath('//ul[@class="list"]/li/div/a/@href'))     
    print(url)
    
# 抓取详细信息
data = list()
for detail_url in detail_list:
    url = root + detail_url
    rsp = requests.get(url=url, headers=headers)
    html = etree.HTML(rsp.text)
    row = dict()
	
	# 获取标题
    row['title'] = html.xpath('//h1[@class="page-title"]/text()')[0].replace(' ', '').replace('\n', '')
	
	# 获取配方
    row['ins'] = dict()
    for r in html.xpath('//div[@class="ings"]//tr[@itemprop]'):
        k = r.find('td[@class="name"]')
        k = etree.tostring(k,encoding='utf-8').decode('utf-8')
        k = re.sub('<.*?>','',k).replace(' ','').replace('\n','')
        v = r.find('td[@class="unit"]').text.replace(' ','').replace('\n','')
        row['ins'][k] = v
		
	# 获取烹饪步骤
    row['steps'] = list()
    for r in html.xpath('//div[@class="steps"]/ol/li'):
        li = dict()
        p = r.find('p[@class="text"]')
        img = r.find('img').get('src') if r.find('img') is not None else ''
        text = etree.tostring(p,encoding='utf-8').decode('utf-8')
        text = re.sub('<.*?>','',text).replace(' ','').replace('\n','')
        li['text'] = text
        li['img'] = img
        row['steps'].append(li)
    data.append(row)
    print(row['title'],url)

# 写入文件
with open('data.json','w') as f:
	f.write(json.dumps(data))
