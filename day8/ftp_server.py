'''
文件服务器
fork server训练
'''

from socket import *
import sys,os
import signal
import time

#全局变量
HOST = '0.0.0.0'
PORT = 14325
ADDR = (HOST,PORT)
FILE_PATH = '/home/tarena/aid1811/RE/'

class FtpServer(object):
    def __init__(self,connfd):
        self.connfd = connfd

    def do_list(self):
        #获取文件列表
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.connfd.send('文件库为空'.encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        #拼接文件为字符串    
        files = ""
        for file in file_list:
            #排除隐藏文件,判断是文件
            if file[0] != '.' and os.path.isfile(FILE_PATH+file):
                files = files + file + ','
        #将拼接好的字符串传给客户端
        self.connfd.send(files.encode())
    
    def do_download(self,filename):
        try:
            fd = open(FILE_PATH+filename,'rb')
        except IOError:
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        #发送文件内容
        while True:
            data = fd.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                fd.close()
                break
            self.connfd.send(data)
    
    def do_upload(self,filename):
        try:
            fw = open(FILE_PATH+filename,'wb')
        except Exception as e:
            self.connfd.send('未知错误'.encode())
            return
        else:
            print('OK')
            self.connfd.send(b'OK')
            while True:
                data = self.connfd.recv(1024)
                if data == b'##':
                    break
                fw.write(data)
            fw.close()


def do_request(connfd):
    ftp = FtpServer(connfd)
    while True:
        data = connfd.recv(1024).decode()
        #退出
        if not data or data[0] == 'Q':
            connfd.close()
            return
        #查看文件列表
        elif data[0] == 'L':
            ftp.do_list()
        #下载文件
        elif data[0] == 'D':
            filename = data.split(' ')[-1]
            ftp.do_download(filename)
        elif data[0] == 'U':
            filename = data.split(' ')[-1]
            ftp.do_upload(filename)

        

#网络搭建
def main():
    #创建监听套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    #处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('ready!')

    while True:
        try:
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('服务器退出')
        except Exception as e:
            print("Error:",e)
            continue
        print(addr,'连接客户端')
        
        #创建子进程处理客户端请求
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            #处理客户端请求
            do_request(connfd)
            os._exit(0)
        #无论父进程或者创建进程失败,都是循环接受新的连接
        else:
            connfd.close()


if __name__ == "__main__":
    main()

