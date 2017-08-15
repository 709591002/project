#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : meitu-2.py
# @Author: Liu
# @Date  : 2017/6/23

import requests
import re

url= 'http://www.mm131.com/xinggan/2373.html'
html=requests.get(url)

user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
headers={'user-agent':user_agent}
#request=urllib2.Request(url,headers=headers)
html=requests.get(url,headers=headers).text #读取整个页面为文本
a= re.search(r'img alt=".*? src="(.*?)" /',html,re.S)
print(a.group(1))

pic=requests.get(a, timeout=2)
fp=open(pic,'wb')
fp.write(pic.content)
fp.close()
