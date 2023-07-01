# coding: utf-8

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
def normal_put(local_path):
    if not os.path.isfile(local_path):
        print("no file")
        return 
    starttime = time.perf_counter()
    j=0
    f = open(local_path, 'rb')
    filename = os.path.split(local_path)[-1]
    chunk_size=1024*1024
    total_size = os.path.getsize(local_path)
    total_chunk = math.ceil(total_size/chunk_size)
    while j<total_chunk:
        block = f.read(1024*1024)
        if not block:
            break
        x = ipArray[random.randint(0,ipnum-1)]
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((x[0], x[1]))
            s.send("put".encode("utf-8"))
            sleep(0.1)
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        header_dic = {
                "filename": filename,
                "total_size": total_chunk,
                "num": j
            }
        header_bytes = json.dumps(header_dic)
        length=len(header_bytes)
        header_bytes_length = struct.pack("i", length)
        s.send(header_bytes_length)
        s.send(header_bytes.encode("utf-8"))
        sleep(0.1)
        s.send(block)
        sleep(1)
        s.close()
        j=j+1

    f.close()
    endtime = time.perf_counter()
    print(round(endtime-starttime),"s",sep='')
    
def normal_get(file):
    starttime = time.perf_counter()
    

    for x in ipArray:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            s.connect((x[0], x[1]))
            s.send("get".encode("utf-8"))
            sleep(0.1)        
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        s.send(file.encode("utf-8"))
        sleep(0.1)   
        print("Waiting...")
        length = struct.unpack("i", s.recv(4))[0]
        
        canum = struct.unpack("i", s.recv(4))[0]
        for i in range(0,canum):
            num = struct.unpack("i", s.recv(4))[0]
            with open("%s%s" % (dir_path,file+"."+str(num)), "wb") as f:
                data = s.recv(1024*1024)
                f.write(data)
        s.close() 
        
    new_file=open("%s%s" % (dir_path,file), "wb")
    new_file=open("%s%s" % (dir_path,file), "ab")
    for i in range(0,length):
        with open("%s%s" % (dir_path,file+"."+str(i)), "rb") as f:
            block = f.read(1024*1024*2)
            new_file.write(block)
    
    
    


    endtime = time.perf_counter()
    print(round(endtime-starttime),"s",sep='')
    
    
    
def super_put(local_path):
    if not os.path.isfile(local_path):
        print("no file")
        return 
    starttime = time.perf_counter()
    j=0
    f = open(local_path, 'rb')
    filename = os.path.split(local_path)[-1]
    chunk_size=1024*1024
    total_size = os.path.getsize(local_path)
    total_chunk = math.ceil(total_size/chunk_size)
    stime=0
    while j<total_chunk:
        x = ipArray[random.randint(0,ipnum-1)]
        try:
            f = open(local_path, 'rb')
            block = f.read(1024*1024*j)
            block = f.read(1024*1024)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((x[0], x[1]))
            s.send("cput".encode("utf-8"))
            sleep(0.1)
            header_dic = {
                    "filename": filename,
                    "total_size": total_chunk,
                    "num": j
                }
            header_bytes = json.dumps(header_dic)
            length=len(header_bytes)
            header_bytes_length = struct.pack("i", length)
            s.send(header_bytes_length)
            s.send(header_bytes.encode("utf-8"))
            sleep(0.1)
            s.send(block)
            sleep(1)
            s.close()
            j=j+1

            f.close()
            endtime = time.perf_counter()
            stime=round(endtime-starttime)+stime
        except socket.error as msg:
            print(msg)

            starttime = time.perf_counter()
            continue
    endtime = time.perf_counter()
    stime=round(endtime-starttime)+stime
    print(stime,"s",sep='')

def super_get(file):
    starttime = time.perf_counter()
    stime=0

    for x in ipArray:
        g_num=0
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                s.connect((x[0], x[1]))
                s.send("cget".encode("utf-8"))
                sleep(0.1)                        
                s.send(file.encode("utf-8"))
                sleep(0.1)   
                print("Waiting...")
                g_num_byte = struct.pack("i", g_num)
                s.send(g_num_byte)
                sleep(0.1)
                
                 
                length = struct.unpack("i", s.recv(4))[0]
                
                canum = struct.unpack("i", s.recv(4))[0]
                
                for i in range(0,canum):
                    num = struct.unpack("i", s.recv(4))[0]
                    with open("%s%s" % (dir_path,file+"."+str(num)), "wb") as f:
                        data = s.recv(1024*1024)
                        f.write(data)
                        g_num=g_num+1
                if(g_num==canum):
                    break
                s.close() 
                endtime = time.perf_counter()
                stime=round(endtime-starttime)+stime
            except socket.error as msg:
                starttime = time.perf_counter()
                print(msg)
        
    new_file=open("%s%s" % (dir_path,file), "wb")              
    new_file=open("%s%s" % (dir_path,file), "ab")
    for i in range(0,length):
        with open("%s%s" % (dir_path,file+"."+str(i)), "rb") as f:
            block = f.read(1024*1024)
            new_file.write(block)

    endtime = time.perf_counter()
    stime=round(endtime-starttime)+stime
    print(stime,"s",sep='')
def check(file):
    for x in ipArray:
        print(x)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            s.connect((x[0], x[1]))
            s.send("check".encode("utf-8"))
            sleep(0.1)
            s.send(file.encode("utf-8"))
            sleep(0.1)
              
            canum = struct.unpack("i", s.recv(4))[0]
            print(canum)
            num_list=[]
            for i in range(0,canum):   
                num = struct.unpack("i", s.recv(4))[0]
                num_list.append(num)
            num_list.sort()
            print(num_list)
                        
        except socket.error as msg:
                print(msg)


    
ipArray=[]
ipnum=3
if __name__ == '__main__':
    ipnum=int(input("ip num:"))

    for i in range(0,ipnum):
        ipadd=str(input("ip:"))
        ipport=int(input("port:"))
        ip=[ipadd,ipport]
        ipArray.append(ip)
        
    
    
    while(1):
        cmd=str(input())
        if not cmd:
            continue
        cmdList=cmd.split()
        if(cmdList[0]=="put"):
            normal_put(cmdList[1])
        elif(cmdList[0]=="get"):
            normal_get(cmdList[1])
        elif(cmdList[0]=="cput"):
            super_put(cmdList[1])
        elif(cmdList[0]=="cget"):
            super_get(cmdList[1])
        elif(cmdList[0]=="check"):
            check(cmdList[1])
        elif(cmdList[0]=="exit"):
            break
        else:
            print(u'no cmd %s'%cmdList[0])
    
    
