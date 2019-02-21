#tcp_client.py

from socket import *

#创建套接字
s = socket()

#发起连接请求
server_addr = ('127.0.0.1',8888)
s.connect(server_addr)

#消息收发
while True:
    data = input(">>")
    if not data:
        break
    s.send(data.encode())
    data = s.recv(1024)
    print("From server:",data.decode())

s.close()







