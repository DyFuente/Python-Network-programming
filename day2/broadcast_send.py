from socket import *
from time import sleep

#目标地址:
dest = ('172.40.71.255',9999)

#创建套接字
s = socket(AF_INET,SOCK_DGRAM)
s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)

data = '1943·代号:凛冬'
while True:
    sleep(2)
    s.sendto(data.encode(),dest)
s.close()
