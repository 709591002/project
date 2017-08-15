#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : doubanmovies.py
# @Author: Liu
# @Date  : 2017/7/3

import requests
from bs4 import BeautifulSoup
import pymongo
import re

client = pymongo.MongoClient('localhost',27017)
douban=client['douban'] #得到一个数据库
top250=douban['top250'] #得到一个数据集合

urls=['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
print ('1111')
def get_info(url):
    wb_data=requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    names=soup.select('div.hd > a')
    #print names
    times=re.findall('<br>(.*?)&nbsp',wb_data.text,re.S)
    places=re.findall('&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;',wb_data.text)
    #print places
    levels=soup.select('span.rating_num')
    #print  levels
    quotes=soup.select('span.inq')
    #print quotes

    for name,time,place,level,quote in zip(names,times,places,levels,quotes):
        info={
            'name':name.get_text().split('/')[0].split('\n')[1],
            'time':time.split('\n')[1].replace(' ',''),
            'place':place,
            'level':level.get_text(),
            'quote':quote.get_text()
        }
        top250.insert_one(info)

for url in urls:
    get_info(url)

