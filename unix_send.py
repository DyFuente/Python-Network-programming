from socket import *

#设置相同的本地套接字文件
sock_file = './sock'

#创建本地套接字
sockfd = socket(AF_UNIX,SOCK_STREAM)

#发起连接
sockfd.connect(sock_file)

#消息收发
while True:
    data = input('>>')
    if not data:
        break
    sockfd.send(data.encode())

#关闭连接
sockfd.close()
