from socket import *
from select import *

#创建要关注的IO
sockfd = socket()
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockfd.bind(('0.0.0.0',14325))
sockfd.listen(10)
#创建poll对象
p = poll()

#建立查找字典
fdmap =  {sockfd.fileno():sockfd}

#注册IO
p.register(sockfd,POLLIN|POLLERR)

#循环监控
while True:
    events = p.poll()    #阻塞
    #遍历列表,处理IO
    for fd,event in events:
        if fd == sockfd.fileno():
            connfd,addr = fdmap[fd].accept()
            print('Connect from',addr)
            #添加新的注册IO
            p.register(connfd,POLLIN|POLLHUP)
            #更新字典
            fdmap[connfd.fileno()] = connfd
        elif event & POLLHUP:
            print('客户端退出')
            p.unregister(fd)    #取消关注
            fdmap[fd].close()
            del fdmap[fd]
        elif event & POLLIN:
            data = fdmap[fd].recv(1024)
            print(data.decode())
            fdmap[fd].send(b'Receive your massage')


