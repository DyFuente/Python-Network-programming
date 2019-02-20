#聊天室服务器
#coding =utf-8
'''
Chatroom
env: python3.5
exc: socket and fork
'''
from socket import *
import os,sys

#保存用户
user = {}

#处理登录
def do_login(sockfd,name,addr):
    if name in user:
        sockfd.sendto('用户已存在'.encode(),addr)
        return
    sockfd.sendto(b"OK",addr)

    #通知其他人
    msg = '欢迎%s加入聊天室'%name
    for i in user:
        sockfd.sendto(msg.encode(),user[i])

    #将用户存入user
    user[name] = addr

#处理聊天
def do_chat(sockfd,name,text):
    msg = "%s: %s"%(name,text)
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(),user[i])

#处理请求
def do_requests(sockfd):
    while True:
        data,addr = sockfd.recvfrom(1024)
        msgList = data.decode().split(' ')
        #处理请求类型
        if msgList[0] == 'L':
            do_login(sockfd,msgList[1],addr)
        elif msgList[0] == 'C':
            #重新组织消息内容
            text = ' '.join(msgList[2:])
            do_chat(sockfd,msgList[1],text)


#创建网络连接
def main():
    ADDR = ('0.0.0.0',14325)
    #创建套接字
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)

    #处理各种客户端请求
    do_requests(sockfd)

if __name__ == '__main__':
    main()
