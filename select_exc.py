from select import select
from socket import *
import sys
from time import ctime

#创建套套接字
sockfd = socket()
sockfd.bind(('0.0.0.0',14325))
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockfd.listen(5)

#日志文件
f = open('log.txt','a')

#添加的关注列表
rlist = [sockfd,sys.stdin]
wlist = []
xlist = []

#监控关注的IO
while True:
    rl,wl,xl = select(rlist,wlist,xlist)
    for r in rl:
        if r is sockfd:
            connfd,addr = r.accept()
            print('Connect from ',addr)
            rlist.append(connfd)
        elif r is sys.stdin:
            #将终端输入的消息存入文件
            f.write("%s %s"%(ctime(),r.readline()))
            #刷新文件缓冲
            f.flush()
        else:
            #接收消息
            data = connfd.recv(1024)
            if not data:
                rlist.remove(r)
                r.close()
                continue
            #将接收的消息存入文件
            f.write("%s %s \n"%(ctime(),data.decode()))
            #刷新文件缓冲
            f.flush()
            connfd.send(b'logging')

