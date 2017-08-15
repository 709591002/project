#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : tupian.py
# @Author: Liu
# @Date  : 2017/6/28

import urllib
import re

def getHtml(url):
    page=urllib.urlopen(url)
    html=page.read()
    return html


def getImg(html):
    reg=r'src="(.+?\.jpg)" size'
    imgre=re.compile(reg)
    imglist=re.findall(imgre,html)
    x=0
    for imgurl in imglist:
        urllib.urlretrieve(imgurl,'%s.jpg' %x)
        x+=1








html=getHtml("http://tieba.baidu.com/p/5186115711?fid=71")
print getImg(html)
