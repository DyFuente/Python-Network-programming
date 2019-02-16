from socket import *
import time

#创建套接字
sockfd = socket(AF_INET,SOCK_DGRAM)

#收发消息

for i in range(2,255):
    HOST = '172.40.71.%d'%i
    PORT = 8888
    ADDR = (HOST,PORT)
    print(ADDR)
    data = 'hello'
    sockfd.sendto(data.encode(),ADDR)
    # msg,addr = sockfd.recvfrom(1024)
    # print('Receive from Server:',msg.decode())
    # time.sleep(0.1)

    #关闭套接字
sockfd.close()