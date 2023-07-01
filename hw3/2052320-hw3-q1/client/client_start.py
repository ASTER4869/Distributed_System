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

taglist=set()
taglist=("article","inproceedings","proceedings","book","incollection","phdthesis"
         ,"mastersthesis","www")
datas=set()
num=6
class MovieHandler(sax.ContentHandler):
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
        if tag in taglist:
            self.key = attributes["key"]
    # 元素结束事件处理
    def endElement(self, tag):
        if tag in taglist:
            # print (self.key)
            # print (self.author)
            # print (self.year)
            if self.year!="":
                n=random.randint(0,num-1)
                
                article=("<article key=\"%s\">\n" %self.key)
                for a in self.author:
                    article+="<author>%s</author>\n" %a
                article+="<year>%s</year>\n" %self.year
                article+="</article>\n"
                #print(article)
                while 1: 
                    try:
                        path=dir_path+"dblp_"+str(n)+".xml"          
                        f = open(path, 'a+')
                        f.write(article)
                        f.close()
                        break
                    except:
                        n=random.randint(0,num-1)
                        print("error")
                    
            self.clear()
        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "author":
            self.author.append(content)
        elif self.CurrentData == "year":
            self.year = content


if (__name__ == "__main__"):
    
    for i in range(num):
        f = open(dir_path+"dblp_"+str(i)+".xml", 'w')
        f.write("<dblp>\n")
        f.close()
    
    
    # 创建一个 XMLReader
    parser = sax.make_parser()
    # turn off namepsaces
    parser.setFeature(sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    parser.parse("dblp.xml")
    


# with open(r'client\dblp.xml', "r") as xml_file:
#         # 读取数据，以树的结构存储
#         tree = ET.parse(xml_file)
#         # 访问树的梗节点
#         root = tree.getroot()
#         # 返回DataFrame格式数据

# f = open(r'client\dblp.xml', 'rb')
# while 1:
#     s=f.read(800)
#     print (s)
#<article mdate="2020-06-25" key="tr/meltdown/s18" publtype="informal">\n<author>Paul Kocher</author>\n<author>Daniel Genkin</author>\n<author>Daniel Gruss</author>\n<author>Werner Haas 0004</author>\n<author>Mike Hamburg</author>\n<author>Moritz Lipp</author>\n<author>Stefan Mangard</author>\n<author>Thomas Prescher 0002</author>\n<author>Michael Schwarz 0001</author>\n<author>Yuval Yarom</author>\n<title>Spectre Attacks: Exploiting Speculative Execution.</title>\n<journal>meltdownattack.com</journal>\n<year>2018