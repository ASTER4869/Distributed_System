# coding: utf-8
import threading
from time import sleep
import socket
import sys
import struct

def fast_result(name):
    with open("record.log",'r') as f1:     # 读文件
            
        s="null"
        for line in f1:        
            line=str(line)
        
            num=line.count(str(name)[2:-1])
            if(num>=1):
                s+=line

    print(s)                   
    return s

            
            
def hash_data(conn, addr,cmd):
    print('Accept new connection from {0}'.format(addr))



    n=fast_result(cmd)
    conn.send(n.encode("utf-8"))


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("192.168.119.1", 3344))
        s.listen(10)
        
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Waiting...")
    
    while True:
        conn, addr = s.accept()
        cmd = conn.recv(8096)
        print (str(cmd))
        t = threading.Thread(target=hash_data, args=(conn, addr,cmd))
        t.start()



if __name__ == '__main__':
    socket_service()