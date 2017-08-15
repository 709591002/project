#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : meizi-1.py
# @Author: Liu
# @Date  : 2017/6/22
import urllib2
import urllib
import re
import os
import sys

class MEIZITU:
    #初始化该类的方法
    def __init__(self,baseUrl):
        self.baseUrl=baseUrl

    def getPage(self,pageNum):
        try:
            url=self.baseUrl+str(pageNum)
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            headers={'user-agent':user_agent}
            request=urllib2.Request(url,headers=headers)
            response=urllib2.urlopen(request)
            #print response.read() #测试输出
            return response.read()#.decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接网页失败，失败原因",e.reason
                return None
    #当前页面的页码
    def getpageNum(self):
        page=self.getPage(1)
        pattern=re.compile('<span class="current-comment-page.*?>(.*?)</span>',re.S)
        result=re.search(pattern,page)
        if result:
            #print result.group(1).strip('[]')
            num=result.group(1).strip('[]')
            return num
        else:
            return None

    def getImg(self):
        pagecode = self.getPage(1)
        reg = r'img src="(.*?)" style='
        pattern = re.compile(reg,re.S)
        images=re.findall(pattern,pagecode)
        #for image in images:
            #print image
        return images #得到图片的地址

    def saveImg(self):
        if not os.path.exists('meizitu'):
            os.mkdir('meizitu')
        subnames=os.walk('meizitu')
        count=0
        for name,subs,pas in subnames:
            count=len(subs)

        print count
        images=self.getImg()
        for image in images:
            print image
            count+=1
            filename=image.split('/')[-1]
            #print "正在保存图片："+filename
            #urllib.urlretrieve(url=image,filename=("meizitu/%s.jpg"%count))
            with (os.path.join('meizi', filename), 'wb') as file:
                file.write(image)
                file.close





baseUrl="http://jandan.net/ooxx/page-"
meizi=MEIZITU(baseUrl)
meizi.getPage(147)
print meizi.getpageNum()
print meizi.getImg()

