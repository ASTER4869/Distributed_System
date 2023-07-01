# coding: utf-8
from time import sleep
import time
import socket
import json
import struct
import threading


def slow_get():
    global num
    num=0
    name=input("input name\n")
    year=input("input year if no input #\n")
    starttime = time.perf_counter()
    thread_list = []
    for i in range(ds_num):
        t = threading.Thread(target=action, args=("slow",i,name,year))
        thread_list.append(t)
        t.start()
        
    for j in thread_list:
        j.join()
       
    endtime = time.perf_counter()
    ss=str(round(endtime-starttime))+"s\n"
    with open("2052320-hw2-q1.log",'a') as f3:     
        f3.write(ss)
    print(round(endtime-starttime),"s",sep='')
num=0    
def action(cmd,i,name,year):
    global num
    t=1
    while t:
        for x in ip_dic[i]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                s.connect((x[0], x[1]))

                header_dic = {
                    "cmd":  cmd,
                    "name": name,
                    "year": year,
                    "i": i
                }
                header_bytes = json.dumps(header_dic) 
                s.send(header_bytes.encode("utf-8"))  
                print("Waiting...")        
                num_ds = struct.unpack("i", s.recv(4))[0]
                num+=num_ds

                s.close() 
                t=0
                break
            except socket.error as msg:
                print(msg)
def fast_get():
    
    global num
    num=0
    name=input("input name\n")
    year=input("input year if no input #\n")
    starttime = time.perf_counter()
    thread_list = []
    for i in range(ds_num):
        t = threading.Thread(target=action, args=("fast",i,name,year))
        thread_list.append(t)
        t.start()
        
    for j in thread_list:
        j.join()
    
    print(num)    
    endtime = time.perf_counter()
    print(round(endtime-starttime),"s",sep='')
    ss=str(round(endtime-starttime))+"s\n"
    with open("2052320-hw2-q1.log",'a') as f3:     
        f3.write(ss)

ds_num=1
ip_dic={}
if __name__ == '__main__':
    with open("record.txt",'r') as f1:     # 读文件
        line = f1.read()
        ip_dic = eval(line)
    try:
        with open("2052320-hw2-q1.log",'r') as f3:     
            pass
    except:
        with open("2052320-hw2-q1.log",'w') as f3:     
            pass
    ds_num=len(ip_dic)   
    while(1):
        print("input type")
        cmd=str(input())
        if not cmd:
            continue
        cmdList=cmd.split()
        if(cmdList[0]=="slow"):
            slow_get()
        elif(cmdList[0]=="fast"):
            fast_get()
        elif(cmdList[0]=="exit"):
            break
        else:
            print(u'no cmd %s'%cmdList[0])