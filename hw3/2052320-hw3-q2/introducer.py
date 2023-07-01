# coding: utf-8
import socket
import sys
from time import sleep
import time

def socket_service():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind(("192.168.119.1", 3333))
        
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting...")
    
    while True:
        data,addr=s.recvfrom(1024)
        print(addr)
        print (str(data))
        while 1:
            try:
                with open("list.txt",'rb') as f1:     # 读文件
                    line = f1.read()
                break
            except:
                print("file used")

                
        s.sendto(line,addr)

if __name__ == '__main__':
    socket_service()