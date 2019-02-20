#聊天室客户端

from socket import *
import os,sys

#服务器地址
ADDR = ('127.0.0.1',14325)

#发消息
def send_msg(sockfd,name):
    while True:
        text = input('发言:')
        msg = "C %s %s"%(name,text)
        sockfd.sendto(msg.encode(),ADDR)

#收消息
def recv_msg(sockfd):
    while True:
        data,addr = sockfd.recvfrom(2048)
        print(data.decode())

#创建网络连接
def main():
    sockfd = socket(AF_INET,SOCK_DGRAM)
    
    while True:
        name = input("请输入姓名:")
        msg = "L "+ name
        #发送请求给服务端
        sockfd.sendto(msg.encode(),ADDR)
        #等待回应
        data,addr = sockfd.recvfrom(1024)
        if data.decode() == 'OK':
            print('您已进入聊天室')
            break
        else:
            print(data.decode())
    
    #创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(sockfd,name)
    else:
        recv_msg(sockfd)


if __name__ == "__main__":
    main()