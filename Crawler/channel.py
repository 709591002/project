#-*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup       #导入库
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url="https://book.douban.com/tag/?icn=index-nav"
wb_data=requests.get(url)  #请求网址
soup=BeautifulSoup(wb_data.text,"lxml") #创建beautiful对象，解析网页信息,并制定解析器lxml
tags=soup.select("#content > div > div.article > div > div > table > tbody > tr > td > a")
#根据CSS路径查找标签信息，CSS路径获取方法，右键-检查-copy selector，tags返回的是一个列表
#get_text()方法：用来获取标签里面的文本内容，在括号里面加"strip=True"可以去除文本前后多余的空格
for tag in tags:
    tag=tag.get_text() #得到 tag 中包含的文本内容(即图书标签的分类文本，如小说，外国文学等）
    helf="https://book.douban.com/tag/"
    #观察一下豆瓣的网址，基本都是这部分加上标签信息，所以我们要组装网址，用于爬取标签详情页
    url=helf+str(tag)
    #print(url) #网址组装完毕，输出

channel='''
https://book.douban.com/tag/小说
https://book.douban.com/tag/外国文学
https://book.douban.com/tag/文学
https://book.douban.com/tag/随笔
https://book.douban.com/tag/中国文学
https://book.douban.com/tag/经典
https://book.douban.com/tag/日本文学
https://book.douban.com/tag/散文
https://book.douban.com/tag/村上春树
https://book.douban.com/tag/诗歌
https://book.douban.com/tag/童话
https://book.douban.com/tag/王小波
https://book.douban.com/tag/杂文
https://book.douban.com/tag/古典文学
https://book.douban.com/tag/儿童文学
https://book.douban.com/tag/名著
https://book.douban.com/tag/张爱玲
https://book.douban.com/tag/余华
https://book.douban.com/tag/当代文学
https://book.douban.com/tag/钱钟书
https://book.douban.com/tag/外国名著
https://book.douban.com/tag/鲁迅
https://book.douban.com/tag/诗词
https://book.douban.com/tag/茨威格
https://book.douban.com/tag/米兰·昆德拉
https://book.douban.com/tag/杜拉斯
'''