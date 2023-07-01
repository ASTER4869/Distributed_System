# coding: utf-8
import pandas as pd
from xml import sax
# 一个轻量的XML解析器
from xml.etree.cElementTree import iterparse
import xml.etree.cElementTree as ET
import os
import threading
from time import sleep
import socket
import sys
import json
import struct
dir_path=os.path.abspath(__file__)
dir_path=dir_path.rstrip(dir_path.split('\\')[-1])
e_year=1920
l_year=2023

y_1=0 
y_2=0
num_s=0 
s_name=""
def fast_result(name,year,lm):

    num=0
    if(year=="#"):
        for i in range(e_year,l_year):
            if(str(i) in s_dic[lm]):
                if(name in s_dic[lm][str(i)]):
                    num+=s_dic[lm][str(i)][name]      
    elif(year[0]=='y'):
        
        if(year[4]=='>'):
            y=int(year[5:])
            for i in range(y+1,l_year):
                if(str(i) in s_dic[lm]):
                    if(name in s_dic[lm][str(i)]):
                        num+=s_dic[lm][str(i)][name]
        elif(year[4]=='<'):
            y=int(year[5:])
            for i in range(e_year,y):
                if(str(i) in s_dic[lm]):
                    if(name in s_dic[lm][str(i)]):
                        num+=s_dic[lm][str(i)][name]
        elif(year[4]=='='):
            y=int(year[5:])
            if(str(y) in s_dic[lm]):
                if(name in s_dic[lm][str(y)]):
                    num+=s_dic[lm][str(y)][name]

    elif(year[5]=='y'):
        y_1=min(int(year[0:4]),int(year[10:]))
        y_2=max(int(year[0:4]),int(year[10:]))
        for i in range(y_1+1,y_2):
            if(str(i) in s_dic[lm]):
                if(name in s_dic[lm][str(i)]):
                    num+=s_dic[lm][str(i)][name]    
                    
    return num

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
        if tag == "article":
            self.key = attributes["key"]
    # 元素结束事件处理
    def endElement(self, tag):
        if tag == "article":
            global y_1,y_2,num_s,s_name
            #print(article)
            if(int(self.year)>y_1 and int(self.year)<y_2):
                if(s_name in self.author):
                    num_s+=1
                
           
                    
            self.clear()
        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "author":
            content= ''.join([i for i in content if not i.isdigit()])
            content=content.strip()

            self.author.append(content)
        elif self.CurrentData == "year":
            
            self.year = content
            
            
              
def slow_result(name,year,file):
    global y_1,y_2,num_s,s_name
    y_1=0 
    y_2=0
    num_s=0
    s_name=name
    if(year=="#"):
        y_1=e_year
        y_2=l_year
    elif(year[0]=='y'):        
        if(year[4]=='>'):
            y_1=int(year[5:])
            y_2=l_year

        elif(year[4]=='<'):
            y_2=int(year[5:])
            y_1=e_year

        elif(year[4]=='='):
            y_1=int(year[5:])-1
            y_2=int(year[5:])+1
    elif(year[5]=='y'):
        y_1=min(int(year[0:4]),int(year[10:]))
        y_2=max(int(year[0:4]),int(year[10:]))
    try:    
        # 创建一个 XMLReader
        parser = sax.make_parser()
        # turn off namepsaces
        parser.setFeature(sax.handler.feature_namespaces, 0)

        # 重写 ContextHandler
        Handler = MovieHandler()
        parser.setContentHandler(Handler)
        parser.parse(file)
    except:
        pass
    return num_s




def slow_data(conn, addr,name,year,i):
    print('Accept new connection from {0}'.format(addr))
    n=slow_result(name,year,"dblp_%s.xml" %i)
    n_pack = struct.pack("i", n)
    conn.send(n_pack)


    
    

def hash_data(conn, addr,name,year,i):
    print('Accept new connection from {0}'.format(addr))

    n=fast_result(name,year,i)
    n_pack = struct.pack("i", n)
    conn.send(n_pack)
    
    
       
def branch(conn, addr):    
    cmd = conn.recv(8096)
    dic = json.loads(cmd)
    print (str(cmd))
    print(dic["cmd"])
    if(dic["cmd"]=='slow'):
        t = threading.Thread(target=slow_data, args=(conn, addr,dic["name"],dic["year"],dic["i"]))
        t.start()
    elif(str(dic["cmd"])=='fast'):
        t = threading.Thread(target=hash_data, args=(conn, addr,dic["name"],dic["year"],dic["i"]))
        t.start()
    
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("192.168.119.1", 3333))
        s.listen(10)
        
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting...")
    
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=branch, args=(conn, addr))
        t.start()


s_dic={}
if __name__ == '__main__':
    
    for i in range(10):
        try:
            with open("dblp_%s.txt"%i,'r') as f1:     # 读文件
                line = f1.read()
                dic = eval(line)
                s_dic[i]=dic
        except:
            pass
    socket_service()