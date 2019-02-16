from socket import *

#创建套接字
sockfd = socket()

#发起连接
# server_addr = ('172.40.91.185',8888)
server_addr = ('127.0.0.1',14325)
sockfd.connect(server_addr)

#收发消息
while True:
    data1 = input('请输入要发送的消息:')
    sockfd.send(data1.encode())
    data = sockfd.recv(1024)
    print('From server:',data.decode())
    if data1 == '##':
        break

sockfd.close()