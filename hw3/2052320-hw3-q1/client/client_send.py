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

def normal_put():

    for i in range(ipnum):
        x = ipArray[i]
        for j in range(ipnum//2+1):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((x[0], x[1]))
                s.send("put".encode("utf-8"))
                sleep(0.1)
                t=(j+i)%ipnum
                f = open("dblp_%s.xml"%t, 'rb')
                filename = "dblp_%s.xml"%t
                chunk_size=1024*1024
                total_size = os.path.getsize("dblp_%s.xml"%t)
                total_chunk = math.ceil(total_size/chunk_size)            
                
                header_dic = {
                        "filename": filename,
                        "total_size": total_chunk,
                    }
                header_bytes = json.dumps(header_dic)
                length=len(header_bytes)
                header_bytes_length = struct.pack("i", length)
                s.send(header_bytes_length)
                sleep(0.1)
                s.send(header_bytes.encode("utf-8"))
                sleep(0.1)
                for k in range(total_chunk):
                    block = f.read(1024*1024)
                    s.send(block)
                    sleep(0.1)
                s.close()
                ip_dic[t].append(x)
            except socket.error as msg:
                print(msg)
                sys.exit(1)
   

    f.close()









ip_dic={}






ipArray=[["192.168.119.1", 3333],["192.168.119.1", 4444],["192.168.119.1", 5555],
         ["192.168.119.1", 6666],["192.168.119.1", 7777],["192.168.119.1", 9999]]
ipnum=6
if __name__ == '__main__':
    for i in range(ipnum):
        ip_dic.update({i:[]})
    # ipnum=int(input("ip num:"))

    # for i in range(0,ipnum):
    #     ipadd=str(input("ip:"))
    #     ipport=int(input("port:"))
    #     ip=[ipadd,ipport]
    #     ipArray.append(ip)
        
        
    normal_put()
    
    with open("record.txt",'w') as f:     # 写文件
            f.write(str(ip_dic))
    
    
    
    
    