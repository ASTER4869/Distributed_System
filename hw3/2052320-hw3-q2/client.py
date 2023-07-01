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
import threading


def fast_get(cmd):
    
    
    name=cmd
    starttime = time.perf_counter()
    num=0

    for x in ip_list:
        while 1:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                s.connect((x[0], x[1]))
            
                s.send(name.encode("utf-8"))
                sleep(0.1)
                
                
                
                print("Waiting...")        
                n=s.recv(1024*1024)
                n=n.decode("utf-8")
                print(n)

                s.close() 
                break
            except socket.error as msg:
                print(msg)


    
    print(num)    
    endtime = time.perf_counter()
    print(round(endtime-starttime),"s",sep='')



ip_list=[]
if __name__ == '__main__':
    with open("record.txt",'r') as f1:     # 读文件
        line = f1.read()
        ip_list = eval(line)
    
    while(1):
        cmd=str(input())
        if not cmd:
            continue
        fast_get(cmd)
