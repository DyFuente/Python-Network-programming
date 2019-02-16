from socket import *
from time import sleep,ctime

sockfd = socket()
sockfd.bind(('0.0.0.0',14325))
sockfd.listen(3)

#设置非阻塞状态行为
sockfd.setblocking(False)

#设置超时时间
sockfd.settimeout(10)

while True:
    print('Waiting for connect...')
    try:
        connfd,addr = sockfd.accept()
    except BlockingIOError:
        sleep(2)
        print('夜来风雨声,花落知多少')
        print('%s connect error'%ctime())
        continue
    except timeout:
        print('timeout......')
    else:
        print('Connect from',addr)

