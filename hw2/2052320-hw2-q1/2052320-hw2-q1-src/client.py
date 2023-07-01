#!/usr/bin/env python3
from asyncio.windows_events import NULL
from pickle import NONE
from bs4 import BeautifulSoup
import urllib.request
import socket
socket.setdefaulttimeout(3)
from treelib import Tree
import networkx as nx
import matplotlib.pyplot as plt 
import datetime

starttime = datetime.datetime.now()

G = nx.DiGraph()
tree = Tree() 
urlList=[]
childList=[]
def popurl(url):
    if url[-1]=='/':
        url= url[:-1]
    return url

def isfind(url):
    if url[:4]=="http":
        return True
    return False

def issameweb(url_a,url_b):
    if url_a[:5]=="https":
        url_a=url_a[8:]
    else:
        url_a=url_a[7:]
    if url_b[:5]=="https":
        url_b=url_b[8:]
    else:
        url_b=url_b[7:]
    for i in range(0,len(url_a)):
        if(url_a[i]=='/'):
            url_a=url_a[:i]
            break
    for j in range(0,len(url_b)):
        if(url_b[j]=='/'):
            url_b=url_b[:j]
            break
    url_aList=url_a.split('.')
    url_bList=url_b.split('.')
    for i in range(0,len(url_aList[-1])):
        if(url_aList[-1][i]=='/'):
            url_aList[-1]=url_aList[-1][:i]
    for i in range(0,len(url_bList[-1])):
        if(url_bList[-1][i]=='/'):
            url_bList[-1]=url_bList[-1][:i]
    url_lenth=min(len(url_aList),len(url_bList))
    num=0
    for i in range(1,url_lenth+1):
        if(url_aList[-i]==url_bList[-i]):
            num=num+1
    if(url_b==url_a):
        return True
    if(num>=3):
        return True
    return False
def listweb(url):
    for i in range(0,len(urlList)):
        if(issameweb(urlList[i],url)):
            return False
    return True
def getedge(url,links):
        for tag in links:
            link = tag.get('href',None)
            if link is not None:
                for hasurl in urlList:
                    if(hasurl==link):
                        G.add_edge(url, hasurl)
                
def getrooturl(url,root):

    try:
        conn = urllib.request.urlopen(url)
    except Exception as e:  
        return
    try:
        html = conn.read()
    except Exception as e:  
        return

    soup = BeautifulSoup(html)
    links = soup.find_all('a')
    getedge(url,links)
    if(tree.depth(root)>=4):
        return
    i=0
    identifierLIST=[]
    tempList=[]
    for tag in links:
        if(i<6):
            link = tag.get('href',None)
            if link is not None:
                if isfind(link):
                    link=popurl(link)
                    if(listweb(link)):
                        urlList.append(link)
                        print (link)
                        tempList.append(link)
                        node=tree.create_node(parent=root.identifier,data=link)
                        G.add_edge(root.data, node.data)
                        identifierLIST.append(node)
                        i=i+1
    j=0
    for node in identifierLIST:
        getrooturl(tempList[j],node)
        j=j+1

 
def maxin_degree(G):
    max=0
    for node in G:
        if(G.in_degree(node)>max):
            max=G.in_degree(node)
    for node in G:
        if(G.in_degree(node)==max):
            return node                  
url = str(input())
urlList.append(url)
node=tree.create_node(data=url)
getrooturl(url,node)

plt.rcParams['figure.figsize']= (12, 6) 
nx.draw(G,nx.spring_layout(G))
plt.savefig((url.split('.'))[1]+".png")
print(G.number_of_nodes())
print(G.number_of_edges())
print(maxin_degree(G))
endtime = datetime.datetime.now()
print((endtime - starttime).seconds , "s",sep='')