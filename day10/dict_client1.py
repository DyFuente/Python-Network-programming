from socket import *
import sys
import getpass

#创建网络连接
def main():
    if len(sys.argv)<3:
        print("argv is error")
        return
    host = sys.argv[1]
    port = int(sys.argv[2])
    addr = (host,port)

    #创建套接字
    s = socket()
    try:
        s.connect(addr)
    except Exception as e:
        print(e)
        return
    #进入一级界面
    while True:
        print('''
        =============weclome==============
        --1.注册　　２．登录　　３．退出--
        ==================================
        ''')
        cmd = input('请输入选项：')
        # print(cmd)
        s.send(cmd.encode())
        if cmd not in ['1','2','3']:
            print('请输入正确选项')
            sys.stdin.flush()#清除标准输入
            continue
        elif cmd == '1':
            do_register(s)#注册功能
        elif cmd == '2':
            do_login(s)#登录功能
        elif cmd == '3':
            s.send(b'E')
            sys.exit('谢谢使用')

def do_register(s):
    while True:
        name = input("User:")
        passwd = getpass.getpass()
        passwd1 = getpass.getpass("Again:")
        if (' ' in name) or (' ' in passwd): 
            print('用户名或密码不能有空格')
            continue
        if passwd != passwd1:
            print('两次密码不一致')
            continue
        
        msg = "R %s %s"%(name,passwd)
        #发送请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print('注册成功')
            return
            #login(s,name)#添加这一句表示直接进入登录装态
        elif data == 'EXISTS':
            print('用户已存在')
        else:
            print('注册失败')
           
def do_login(s): 
    name = input('User:')
    passwd = getpass.getpass()
    msg = "L %s %s"%(name,passwd)
    #发送请求
    s.send(msg.encode())#发送给服务器验证
    #等待回复
    data = s.recv(128).decode()
    if data == 'OK':
        print('登陆成功')
        login(s,name)
    else:
        print('登录失败')
            
def login(s,name):
    while True:
        print('''
            ==============================
            --1.查词  2.历史记录 3.注销--
            ==============================
            ''')
        cmd = input('请输入选项：')
        s.send(cmd.encode())
        if cmd not in ['1','2','3']:
            print('请输入正确选项')
            sys.stdin.flush()#清除标准输入
            continue
        elif cmd == '1':
            do_query(s,name)
        elif cmd == '2':
            do_history(s,name)
        elif cmd == '3':
            return

def do_query(s,name):
    while True:
        word = input('请输入要查询的单词：')
        if word == "##":
            break
        msg = "Q %s %s"%(name,word)
        s.send(msg.encode())
        data = s.recv(2018).decode()
        # print(data)
        if data == 'FAIL':
            print('没有找到该单词')      
        else:
            print(data)
            


def do_history(s,name):
        msg = "H %s"%name
        print('')
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            while True:
                data = s.recv(1024).decode()
                if data == '##':
                    break
                print(data)
        else:
            print('没有历史记录')





if __name__ == '__main__':
    main()