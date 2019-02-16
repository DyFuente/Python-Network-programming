from socket import *
from select import select

#创建套接字作为关注的IO
sockfd = socket()
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockfd.bind(('0.0.0.0',14325))
sockfd.listen(5)

#添加的关注列表
rlist = [sockfd]
wlist = []
xlist = [sockfd]

#监控关注的IO
while True:
    rs,ws,xs = select(rlist,wlist,xlist)
    #遍历返回值列表,确定就绪的IO    
    for r in rs:
        #sockfd就绪,有客户端请求连接
        if r is sockfd:
            connfd,addr = r.accept()
            print('Connect from ',addr)
            #将客户端连接套接字加入关注列表
            rlist.append(connfd)
        #表示某个客户端发消息则connfd就绪
        else:
            data = r.recv(1024)
            if not data:
                rlist.remove(r)
                r.close()
                continue
            print('Receive:',data.decode())
            # r.send("木偶".encode())
            #当r放入wlist表示希望主动操作r这个IO
            wlist.append(r)

    for w in ws:
        w.send(b'ok,thanks')
        wlist.remove(w)

    for x in xs:
        pass