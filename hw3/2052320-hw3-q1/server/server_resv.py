# -*- coding=utf-8 -*-
from faulthandler import cancel_dump_traceback_later
import socket
import threading
import sys
import os
import struct
import socket
import json
import struct
import csv
from time import sleep
dir_path=os.path.abspath(__file__)
dir_path=dir_path.rstrip(dir_path.split('\\')[-1])


def deal_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))

    header_bytes_length = struct.unpack("i", conn.recv(4))[0]
    header_bytes_size = 0
    header_bytes = b""
    while header_bytes_size < header_bytes_length:
        data = conn.recv(header_bytes_length)
        header_bytes += data
        header_bytes_size += len(data)
    header_dic = json.loads(header_bytes)
    print(header_dic)
    with open("%s%s" % (dir_path,header_dic["filename"]), "wb") as f:
        pass
    with open("%s%s" % (dir_path,header_dic["filename"]), "ab") as f:
        for i in range(int(header_dic["total_size"])):
            data = conn.recv(1024*1024)
            f.write(data)
    
    f.close()












def socket_service():
    # ipadd=str(input("input ip:"))
    # ipport=int(input("input port:"))
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
        cmd = conn.recv(8096)
        print (str(cmd))
        if(cmd==b'put'):
            t = threading.Thread(target=deal_data, args=(conn, addr))
            t.start()



if __name__ == '__main__':
    socket_service()