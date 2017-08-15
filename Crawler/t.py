#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : t.py
# @Author: Liu
# @Date  : 2017/7/5


import pymongo
client = pymongo.MongoClient('localhost', 27017)
db = client.mydb
collection = db['my_collection']
db.collection_names()