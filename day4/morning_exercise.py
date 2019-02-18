#TCP --面向连接的传输 -- 可靠 -- 流式套接字
#UDP -- 面向无连接的传输 -- 不可靠 -- 数据报套接字

#TCP
from socket import *
#创建套接字
t = socket()
t.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
t.bind(('0.0.0.0',14325))
t.listen(5)

connfd,addr = t.accept()
print('Connect from',addr)
data = connfd.recv(1024)
print(data.decode())
connfd.send(b'OK')

#关闭连接
connfd.close()
sockfd.close()

#创建套接字u
u= socket(AF_INET,SOCK_DGRAM)
#绑定地址
u.bind(('0.0.0.0',14325))
#消息收发
data,addr = u.recvfrom(1024)
print('Connect from%s:%s',%(addr,data.decode()))
u.sendto(b'Ojbk',addr)

#关闭连接
u.close() 