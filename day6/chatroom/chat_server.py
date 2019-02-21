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
    if (name in user) or name == "管理员消息":
        sockfd.sendto('用户已存在'.encode(),addr)
        return
    sockfd.sendto(b"OK",addr)

    #通知其他人
    msg = '\n欢迎%s加入聊天室'%name
    for i in user:
        sockfd.sendto(msg.encode(),user[i])

    #将用户存入user
    user[name] = addr

#处理聊天
def do_chat(sockfd,name,text):
    msg = "\n%s: %s"%(name,text)
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(),user[i])

#用户退出
def do_quit(sockfd,name,addr):
    sockfd.sendto('##'.encode(),addr)
    #删除用户
    del user[name]
    #发送给其他用户
    msg = "\n%s已退出"%name
    for i in user:
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
        elif msgList[0] == 'Q':
            do_quit(sockfd,msgList[1],addr)


#创建网络连接
def main():
    ADDR = ('0.0.0.0',14325)
    #创建套接字
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)

    #创建单独进程用于发送管理员消息
    pid = os.fork()
    if pid < 0:
        print('Error')
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息:")
            msg = "C 管理员消息 "+msg
            sockfd.sendto(msg.encode(),ADDR)

    else:
        #处理各种客户端请求
        do_requests(sockfd)



if __name__ == '__main__':
    main()
