from socket import * 
import os,sys
import signal

#处理客户端请求
def client_handle(connfd):
    print('cilient:',connfd.getpeername())
    while True:
        data = connfd.recv(1024)
        if not data:
            break
        print(data.decode())
        connfd.send(b"Receive your msg")
    connfd.close()
    

#创建监听套接字
HOST = '0.0.0.0'
PORT = 14325
ADDR = (HOST,PORT)
sockfd = socket()
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockfd.bind(ADDR)
sockfd.listen(5)

#处理僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
print('Listen to part 14325...')

#循环等待客户端连接
while True:
    try:
        connfd,addr = sockfd.accept()
    except KeyboardInterrupt:
        sys.exit('服务器退出')
    except Exception as e:
        print("Error:",e)
        continue
    
    #创建子进程处理客户端请求
    pid = os.fork()
    if pid == 0:
        sockfd.close()
        #处理客户端请求
        client_handle(connfd)
        os._exit(0)
    #无论父进程或者创建进程失败,都是循环接受新的连接
    else:
        connfd.close()
