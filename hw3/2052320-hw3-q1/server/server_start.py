# coding: utf-8
import pandas as pd
from xml import sax
# 一个轻量的XML解析器
from xml.etree.cElementTree import iterparse
import xml.etree.cElementTree as ET
import re
import os
from time import sleep
import time
import random
import socket
import sys
import math
import json
import struct
dir_path=os.path.abspath(__file__)
dir_path=dir_path.rstrip(dir_path.split('\\')[-1])


year_set=set()
class YearHandler(sax.ContentHandler):
    def __init__(self):
        self.key = ""
        self.year=""

    def clear(self):
        self.key = ""
        self.year=""
    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "article":
            self.key = attributes["key"]
    # 元素结束事件处理
    def endElement(self, tag):
        if tag == "article":        
            self.clear()
        self.CurrentData = ""
    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "year":
            year_set.add(content)


class DicHandler(sax.ContentHandler):
    def __init__(self):
        self.key = ""
        self.author = []
        self.year=""

    def clear(self):
        self.key = ""
        self.author = []
        self.year=""
    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "article":
            self.key = attributes["key"]
    # 元素结束事件处理
    def endElement(self, tag):
        if tag == "article":
            for name in  self.author:
                name= ''.join([i for i in name if not i.isdigit()])
                name=name.strip()
                if name=="Frank Manola":
                    pass
                if name in content_dic[self.year]:
                    content_dic[self.year][name]+=1
                else:
                    content_dic[self.year][name]=1
            self.clear()
        self.CurrentData = ""
    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "author":
            self.author.append(content)
        elif self.CurrentData == "year":
            self.year = content



num=10
content_dic={}
if (__name__ == "__main__"):
    
    
    for i in range(num):
        try:
            with open("dblp_%s.xml" %i,'r') as f:     # 写文件
                pass
        except:
            continue
        # 创建一个 XMLReader
        parser = sax.make_parser()
        # turn off namepsaces
        parser.setFeature(sax.handler.feature_namespaces, 0)
        try:
            # 重写 ContextHandler
            Handler = YearHandler()
            parser.setContentHandler(Handler)
            parser.parse("dblp_%s.xml" %i)
        except:
            pass
        content_dic={}
        for year in year_set:
            content_dic.update({year:{}})
            
            
            
        try:    
            s_parser = sax.make_parser()
            # turn off namepsaces
            s_parser.setFeature(sax.handler.feature_namespaces, 0)
            
            Handler = DicHandler()
            s_parser.setContentHandler(Handler)
            s_parser.parse("dblp_%s.xml" %i)
        except:
            pass
        
        with open("dblp_%s.txt" %i,'w') as f:     # 写文件
            f.write(str(content_dic))
             
        # with open("dblp_%s.txt" %i,'r') as f1:     # 读文件
        #     line = f1.read()
        #     dic = eval(line)
            
            
        

    






