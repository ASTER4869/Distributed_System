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
# 接收字典字符串
    header_bytes_size = 0
    header_bytes = b""
    while header_bytes_size < header_bytes_length:
        data = conn.recv(header_bytes_length)
        header_bytes += data
        header_bytes_size += len(data)
    header_dic = json.loads(header_bytes)
    print(header_dic)
    with open("%s%s" % (dir_path,header_dic["filename"]+"."+str(header_dic["num"])), "wb") as f:
            data = conn.recv(1024*1024)
            f.write(data)
    
    print(dir_path)
    f.close()
    map_info = {
                "filename": header_dic["filename"],
                "total_size": header_dic["total_size"],
                "num": header_dic["num"],
                "dir_path":dir_path+header_dic["filename"]+"."+str(header_dic["num"])
            }
    header = ['filename', 'total_size', 'num','dir_path']
    try:
        with open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='') as file_obj:
            dictWriter = csv.DictWriter(file_obj, header)            
    except:
        with open("%s" % (dir_path+"record.csv"), 'w', encoding='utf-8', newline='') as file_obj:
            dictWriter = csv.DictWriter(file_obj, header) 
            dictWriter.writeheader()

    with open("%s" % (dir_path+"record.csv"), 'a', encoding='utf-8', newline='') as file_obj:
        dictWriter = csv.DictWriter(file_obj, header)
        dictWriter.writerow(map_info)

def load_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))

    header = ['filename', 'total_size', 'num','dir_path']
    try:
        with open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='') as file_obj:
            dict = csv.DictReader(file_obj, header)            
    except:
        return "no file"
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)
    filename = conn.recv(1024)
    filename=filename.decode("utf-8")
    for row in dict:
        if(row["filename"]==filename):
            length = struct.pack("i", int(row["total_size"]))
            conn.send(length)
            break
    j=0
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)
    for row in dict:
        if(str(row["filename"])==filename):
            j=j+1
    canum = struct.pack("i", j)
    conn.send(canum )
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)   
    for row in dict:
        if(row["filename"]==filename):
            num= struct.pack("i", int(row["num"]))
            conn.send(num)
            f = open(row["dir_path"], 'rb')
            block = f.read(1024*1024)
            conn.send(block)
            sleep(0.1)




def stop_load_data(conn, addr):
    print('Accept new connection from {0}'.format(addr))

    header = ['filename', 'total_size', 'num','dir_path']
    try:
        with open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='') as file_obj:
            dict = csv.DictReader(file_obj, header)            
    except:
        return "no file"
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)
    filename = conn.recv(1024)
    filename=filename.decode("utf-8")
    g_num = struct.unpack("i", conn.recv(4))[0]
    
    for row in dict:
        if(row["filename"]==filename):
            length = struct.pack("i", int(row["total_size"]))
            conn.send(length)
            break
    j=0
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)
    for row in dict:
        if(str(row["filename"])==filename):
            j=j+1
    canum = struct.pack("i", j)
    conn.send(canum )
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)
    i=0   
    for row in dict:
        if(row["filename"]==filename):
            i=i+1
            
            num= struct.pack("i", int(row["num"]))

            f = open(row["dir_path"], 'rb')
            block = f.read(1024*1024)
            if(i>g_num):
                conn.send(num)
                conn.send(block)
                sleep(0.1)

def check(conn, addr):
    print('Accept new connection from {0}'.format(addr))
    header = ['filename', 'total_size', 'num','dir_path']
    try:
        with open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='') as file_obj:
            dict = csv.DictReader(file_obj, header)            
    except:
        return "no file"
    filename = conn.recv(1024)
    filename=filename.decode("utf-8")
    
    
    
    j=0
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)
    for row in dict:
        if(str(row["filename"])==filename):
            j=j+1
    canum = struct.pack("i", j)
    conn.send(canum)
    
    
    file_obj=open("%s" % (dir_path+"record.csv"), 'r', encoding='utf-8', newline='')
    dict = csv.DictReader(file_obj, header)
    for row in dict:
        if(row["filename"]==filename):            
            num= struct.pack("i", int(row["num"]))
            conn.send(num)

    

def socket_service():
    ipadd=str(input("input ip:"))
    ipport=int(input("input port:"))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ipadd, ipport))
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
        elif(cmd==b'get'):
            t = threading.Thread(target=load_data, args=(conn, addr))
            t.start()
        elif(cmd==b'cput'):
            t = threading.Thread(target=deal_data, args=(conn, addr))
            t.start()
        elif(cmd==b'cget'):
            t = threading.Thread(target=stop_load_data, args=(conn, addr))
            t.start()
        elif(cmd==b'check'):
            t = threading.Thread(target=check, args=(conn, addr))
            t.start()


if __name__ == '__main__':
    socket_service()
