#ftp客户端
from socket import *
import sys,os
import time


#具体功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
    
    def do_list(self):
        #发送请求
        self.sockfd.send(b'L')
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split(',')
            for file in files:
                print(file)
        else:
            #无法完成操作
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit('谢谢使用')
    
    def do_download(self,filename):
        #发送下载请求
        self.sockfd.send(('D '+filename).encode())
        #等待反馈
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            fd = open(filename,'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b"##":
                    break
                fd.write(data)
            fd.close()
            print('下载完成')
        else:
            print(data)
        
    def do_upload(self,filename):
        #发送上传请求
        self.sockfd.send(('U '+filename).encode())
        #等待反馈
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            try:
                fd = open(filename,'rb')
            except IOError:
                print('文件不存在')
                return
            else:
                while True:
                    data = fd.read(1024)
                    if not data:
                        time.sleep(0.1)
                        self.sockfd.send(b'##')
                        fd.close()
                        print('上传完成')
                        break
                    else:
                        self.sockfd.send(data)
        else:
            print(data)

#网络连接
def main():
    #服务器地址
    ADDR = ('127.0.0.1',14325)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("连接服务器失败:",e)
        return
    
    ftp = FtpClient(sockfd)
    while True:
        print('''
        ++++++++++++++++ftp+++++++++++++++++
            请选择:
                1. list
                2. download file
                3. upload file
                4. quit
        ++++++++++++++++ftp+++++++++++++++++
        ''')
        cmd = input('请输入命令>>')
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:8] == 'download':
            #将文件名字取出
            filename = cmd.strip().split(' ')[-1]
            ftp.do_download(filename)
        elif cmd[:6] == 'upload':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_upload(filename)
        elif cmd.strip() == 'quit':
            ftp.do_quit()
            break
        else:
            print('请正确输入!')
        


if __name__ == "__main__":
    main()