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
from threading import Timer
dir_path=os.path.abspath(__file__)
dir_path=dir_path.rstrip(dir_path.split('\\')[-1])




def start(s):
    global ip

    s.sendto("join".encode("utf-8"),introducer_ip)
    _,port=s.getsockname()
    ip=(socket.gethostbyname(socket.gethostname()),port)

    print(ip)
    while 1:        
        data,addr=s.recvfrom(2048)
        if(addr==introducer_ip):
            with open("list.txt", "wb") as f:
                f.write(data)
            break


def join():
    global ip
    with open("list.txt", "rb") as f:
        data=f.readline()
        ip_list=eval(data)
    ip_list.append(ip)
    with open("list.txt", "w") as f:
        f.write(str(ip_list))
        f.write('\n')
        f.write(str(int(round(time.time() * 1000))))


def heart_beat(s):
    global ip

    while 1:
        if(random.randint(1,100)>=percent):
            try:
                with open("list.txt", "rb") as f:
                    data=f.readline()
                    ip_list=eval(data)
                f.close()
                with open("list.txt", "rb") as f:
                    data=f.read()
                f.close()
                for i in range(len(ip_list)):
                    if(ip_list[i]==ip):
                        if(ip_list[(i+1)%len(ip_list)]!=ip):
                            s.sendto(data,ip_list[(i+1)%len(ip_list)])
                        if(ip_list[(i+1)%len(ip_list)]!=ip):    
                            s.sendto(data,ip_list[(i+2)%len(ip_list)])
                sleep(0.1)
            except:
                pass
def alive_killer(write_list):
    global ip,acc_iplist

    for i in range(len(write_list)):
        if(write_list[i]==ip):
            if(write_list[(i-1+3*len(write_list))%len(write_list)] in acc_iplist
               and write_list[(i-2+3*len(write_list))%len(write_list)] in acc_iplist):
                pass
            else:
                if(write_list[(i-1+3*len(write_list))%len(write_list)] not in acc_iplist and 
                   write_list[(i-1+3*len(write_list))%len(write_list)]!=ip):
                    with open("record.log", "a") as f:
                        f.write("%s failure\n"%str(write_list[(i-1+3*len(write_list))%len(write_list)]))
                    
                    
                    write_list.remove(write_list[(i-1+3*len(write_list))%len(write_list)])
                    with open("list.txt", "w") as f:
                        f.write(str(write_list))
                        f.write('\n')
                        f.write(str(int(round(time.time() * 1000))))
                    break
                elif(write_list[(i-2+3*len(write_list))%len(write_list)] not in acc_iplist and
                     write_list[(i-2+3*len(write_list))%len(write_list)]!=ip):
                    
                    with open("record.log", "a") as f:
                        f.write("%s failure\n"%str(write_list[(i-2+3*len(write_list))%len(write_list)]))
   
                    
                    write_list.remove(write_list[(i-2+3*len(write_list))%len(write_list)])

                    with open("list.txt", "w") as f:
                        f.write(str(write_list))
                        f.write('\n')
                        f.write(str(int(round(time.time() * 1000))))
                    break
    acc_iplist=[]
        
                    
def action():
    sleep(5) 
    while 1:
        with open("list.txt", "rb") as f:
            line=f.readline()
            write_list=eval(line)
        alive_killer(write_list)
        sleep(2)      

def write_log(node,msg):
    with open("record.log", "a") as f:
        t=str(node)+" "+msg+"\n"
        f.write(t)      
def write_join_log():
    global str_data
    sleep(2) 
    while 1:
        with open("list.txt", "rb") as f:
            ex=f.read()
        f.close()
        with open("list.txt", "rb") as f:
            line=f.readline()
            write_list=eval(line)
            o_timestamp=f.readline()
        f.close()
        str_data=str(ex)
        if(len(str_data)>13):
            list=eval(str_data[2:-18])
            for node in acc_iplist:
                if node not in  list and node != ip:
                    write_log(node,"join")
            str_data=""
            sleep(2) 
def  hear_heart_beat(s):
    global str_data

    while 1:
        try:
            data,addr=s.recvfrom(2048)
            if(len(data)<20):
                write_list.remove(addr)
                with open("list.txt", "w") as f:
                    f.write(str(write_list))
                    f.write('\n')
                    f.write(str(data)[8:21])
                write_log(addr,"leave")
                continue
            if(addr not in acc_iplist):
                acc_iplist.append(addr) 
                if(addr != ip):          
                    t1 = threading.Thread(target=write_log, args=(addr,"connect"))
                    t1.start()
            str_data=str(data)
            timestamp=str_data[-14:-1]
            with open("list.txt", "rb") as f:
                line=f.readline()
                write_list=eval(line)
                o_timestamp=f.readline()
            f.close()

            if(int(o_timestamp)<int(timestamp)):
                with open("list.txt", "wb") as f:
                    f.write(data)



        except:
            pass
def  leave(s):
    sleep(2)
    with open("list.txt", "rb") as f:
        data=f.readline()
        ip_list=eval(data)
    f.close()
    while 1:
        cmd=str(input())
        if(cmd=="leave"):            
            for i in range(len(ip_list)):
                s.sendto(("leave %s"%str(int(round(time.time() * 1000)))).encode("utf-8"),ip_list[i])
        sys.exit()   
def get_udp_port():
    #获取端口号
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(("",0))
    _,port=s.getsockname()
    s.close()
    return port
def out():
    while 1:
        with open("list.txt", "rb") as f:
            line=f.readline()
            write_list=eval(line)
            o_timestamp=f.readline()
        f.close()
        print(write_list)
        print(o_timestamp)
        sleep(2)
introducer_ip=("192.168.119.1", 3333)
ip_list=[]
ip=()
acc_iplist=[]
str_data=""
percent=0
if __name__ == '__main__':
    percent=int(input("输入丢包率:\n"))
    try:
        with open("record.log", "rb") as f:
            pass
    except:
        with open("record.log", "wb") as f:
            pass
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    start(s)
    join()
    t1 = threading.Thread(target=heart_beat, args=(s,))
    t2 = threading.Thread(target=hear_heart_beat, args=(s,))
    t3 = threading.Thread(target=action)
    t4 = threading.Thread(target=write_join_log)
    t5 = threading.Thread(target=leave, args=(s,))
    t6 = threading.Thread(target=out)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    # heart_beat()