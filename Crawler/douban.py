#-*- coding: UTF-8 -*-
'''
import requests
import re
from bs4 import BeautifulSoup
import random
import time
import pymysql
from channel import channel

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#提取评价人数的函数，如果评价人数少于十人，按十人处理
def ceshi_person(person):
    try:
        person=int(person.get_text().split()[0][1:len(person.get_text().split()[0]) - 4])
    except ValueError:
        person=int(10)
        return person

#分情况提取价格的函数，用正则表达式找到含有特殊字符的信息，并换算为“元”
def ceshi_priceone(detil):
    price=detil.get_text().split("/",4)[4].split()
    if re.match("USD",price[0]):
        price=float(price[1])*6
    elif re.match("CNY",price[0]):
        price=price[1]
    elif re.match("\A$",price[0]):
        price=float(price[1:len(price)])*6
    else:
        price=price[0]
    return price


def ceshi_pricetwo(detil):
    price = detil.get_text().split("/", 3)[3].split()
    if re.match("USD", price[0]):
        price = float(price[1]) * 6
    elif re.match("CNY", price[0]):
        price = price[1]
    elif re.match("\A$", price[0]):
        price = float(price[1:len(price)]) * 6
    else:
        price = price[0]
    return price


def mians(url):
    #url="https://book.douban.com/tag/科技"
    wb_data = requests.get(url)
    soup=BeautifulSoup(wb_data.text.encode("utf-8"),"lxml")
    tag=url.split("?")[0].split("/")[-1] #从链接里面提取标签信息，方便存储,此时的标签信息就是科技
    detils=soup.select("ul >  li >  div.info > div.pub") #获取作者，出版社信息，稍后用split函数分离出来
    scors=soup.select("ul > li > div.info > div.star.clearfix > span.rating_nums") #获取评分信息
    persons = soup.select("ul > li > div.info > div.star.clearfix > span.pl") #评价人数
    titles= soup.select("ul > li > div.info > h2 > a") #id名前加#的方法来筛选元素 #书名



    #以上抓取的都是我们需要的html语言标签信息，我们还需要将他们一一分离出来
    for detil,scor,person,title in zip(detils,scors,persons,titles):
        #用zip函数实现一次遍历
        # 因为一些标签中有译者信息，一些标签中没有，为避免错误，所以我们要用一个try来把他们分开执行
        try:
            l=[]#建立一个列表用于存放数据
            author=detil.get_text().split("/",4)[0].split()[0]  #这是含有译者信息的提取办法，根据“/”  把标签分为五部分，然后依次提取出来
            yizhe=detil.get_text().split("/",4)[1]
            publish=detil.get_text().split("/",4)[2]
            time=detil.get_text().split("/",4)[3].split()[0] #时间我们只提取了出版年份
            price=ceshi_priceone(detil) ##因为价格的单位不统一，我们用一个函数把他们换算为“元”
            scoe=scor.get_text()
            person=ceshi_person(person)
            title=title.get_text().split()[0]
        # 当没有译者信息时，会显示IndexError，我们分开处理
        except IndexError:
            try:
                author=detil.get_text().split("/",3)[0].split()[0]
                yizhe = "" ##将detil信息划分为4部分提取，译者信息直接设置为空，其他与上面一样
                publish = detil.get_text().split("/", 3)[1]
                time = detil.get_text().split("/", 3)[2].split()[0].split("-")[0]
                price = ceshi_pricetwo(detil)
                scoe = scor.get_text()
                person = ceshi_person(person)
                title = title.get_text().split()[0]
            except (IndexError, TypeError):
                continue
        ##出现其他错误信息，忽略，继续执行（有些书目信息下会没有出版社或者出版年份，但是数量很少，不影响我们大规模爬取，所以直接忽略）
        except TypeError:
            continue

        l.append([title,scoe,author,price,time,publish,person,yizhe,tag]) #将爬取的数据依次填入列表中
        sql = "INSERT INTO allbooks values(%s,%s,%s,%s,%s,%s,%s,%s,%s)" #这是一条sql插入语句
        cur.executemany(sql,l) #执行sql语句，并用executemary()函数批量插入数据库中
        conn.commit()
#主函数结束

#将Python连接到MySQL中的Python数据库
conn=pymysql.connect(user="root",password="1991",database="python",charset="utf-8")
cur=conn.cursor()

cur.execute('DROP TABLE IF EXISTS allbook') #如果数据库中有allbooks的数据库则删除
sql="""CREATE TABLE allbook(
        title CHAR(255) NOT NULL,
        scor CHAR(255),
        author CHAR(255),
        time CHAR(255),
        publish CHAR(255),
        person CHAR(255),
        yizhe CHAR(255),
        tag CHAR(255)
        )"""

cur.execute(sql) #执行sql语句，新建一个allbooks的数据库

start=time.clock() #设置一个时钟，这样我们就能知道我们爬取了多长时间了
for urls in channel.split():
    urlss=[urls+"?start={}&type=T".format(str(i)) for i in range(0,980,20)]  #从channel中提取url信息，并组装成每一页的链接
    for url in urls:
        mians(url) #执行主函数，开始爬取
        print('11111111111')
        print(url) #输出要爬取的连接，这里我们就知道爬到哪儿了，发生错误也好处理
        time.sleep(int(format(random.randint(0,9))))  #设置一个随机数时间，每爬一个网页可以随机的停一段时间，防止IP被封

end=time.clock()
print('Time Usage:',end-start) #输出爬取的时间
count=cur.execute('select * from allbooks')
print('has %s record' % count) #输出爬取的总数目条数

#释放数据库
if cur:
    cur.close()
if conn:
    conn.close()
'''

import requests
from bs4 import BeautifulSoup
import time
import re
import pymysql
from channel import channel   #这是我们第一个程序爬取的链接信息
import random

def ceshi_person(person):

     try:

         person = int(person.get_text().split()[0][1:len(person.get_text().split()[0]) - 4])
     except ValueError:

         person = int(10)
     return person

def ceshi_priceone(detil):
        price = detil.get_text().split("/", 4)[4].split()
        if re.match("USD", price[0]):
                 price = float(price[1]) * 6
        elif re.match("CNY", price[0]):
                 price = price[1]
        elif re.match("\A$", price[0]):
                 price = float(price[1:len(price)]) * 6
        else:
                 price = price[0]
        return price

def ceshi_pricetwo(detil):
       price = detil.get_text().split("/", 3)[3].split()
       if re.match("USD", price[0]):
               price = float(price[1]) * 6
       elif re.match("CNY", price[0]):
               price = price[1]
       elif re.match("\A$", price[0]):
               price = float(price[1:len(price)]) * 6
       else:
               price = price[0]
       return price


#这是上面的那个测试函数，我们把它放在主函数中
def mains(url):

  wb_data = requests.get(url)
  soup = BeautifulSoup(wb_data.text.encode("utf-8"), "lxml")
  tag=url.split("?")[0].split("/")[-1]
  detils=soup.select("#subject_list > ul > li > div.info > div.pub")
  scors=soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.rating_nums")
  persons=soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.pl")
  titles=soup.select("#subject_list > ul > li > div.info > h2 > a")
  for detil,scor,person,title in zip(detils,scors,persons,titles):
        l = []  #建一个列表，用于存放数据
        try:
             author=detil.get_text().split("/",4)[0].split()[0]
             yizhe= detil.get_text().split("/", 4)[1]
             publish=detil.get_text().split("/", 4)[2]
             time=detil.get_text().split("/", 4)[3].split()[0].split("-")[0]
             price=ceshi_priceone(detil)
             scoe=scor.get_text() if True else ""
             person=ceshi_person(person)
             title=title.get_text().split()[0]
        except IndexError:
              try:
                   author=detil.get_text().split("/", 3)[0].split()[0]
                   yizhe=""
                   publish=detil.get_text().split("/", 3)[1]
                   time=detil.get_text().split("/", 3)[2].split()[0].split("-")[0]
                   price=ceshi_pricetwo(detil)
                   scoe=scor.get_text() if True else ""
                   person=ceshi_person(person)
                   title=title.get_text().split()[0]
              except (IndexError,TypeError):
                    continue

        except TypeError:
         continue


  l.append([title, scoe, author, price, time, publish, person, yizhe, tag])
      # 将爬取的数据依次填入列表中
  sql="INSERT INTO allbooks values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"  #这是一条sql插入语句
  cur.executemany(sql,l)   #执行sql语句，并用executemary()函数批量插入数据库中
  conn.commit()

#主函数到此结束


# 将Python连接到MySQL中的python数据库中
conn = pymysql.connect( user="root",password="1991",database="python",charset='utf8')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS allbooks')   #如果数据库中有allbooks的数据库则删除
sql = """CREATE TABLE allbooks(      
        title CHAR(255) NOT NULL,      
        scor CHAR(255),      
        author CHAR(255),     
        price CHAR(255),     
        time CHAR(255),    
        publish CHAR(255),     
        person CHAR(255),     
        yizhe CHAR(255),     
        tag CHAR(255)       
 )"""
cur.execute(sql)  #执行sql语句，新建一个allbooks的数据库


start = time.clock()   #设置一个时钟，这样我们就能知道我们爬取了多长时间了
for urls in channel.split():
  urlss=[urls+"?start={}&type=T".format(str(i)) for i in range(0,980,20)]   #从channel中提取url信息，并组装成每一页的链接
  for url in urlss:

      mains(url)       #执行主函数，开始爬取
      print(url)        #输出要爬取的链接，这样我们就能知道爬到哪了，发生错误也好处理
      time.sleep(int(format(random.randint(0,9))))   #设置一个随机数时间，每爬一个网页可以随机的停一段时间，防止IP被封
end = time.clock()
print('Time Usage:', end - start)    #爬取结束，输出爬取时间
count = cur.execute('select * from allbooks')
print('has %s record' % count)       #输出爬取的总数目条数

# 释放数据连接
if cur:
     cur.close()
if conn:
     conn.close()



