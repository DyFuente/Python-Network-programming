''' 
    modulses:pymysql
    this is a dict project for AID
'''


from socket import *
import pymysql
import os
import sys
import time
import signal

#定义一些全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#网络搭建
def main():
    #创建数据库连接
    db=pymysql.connect('localhost','root','123456',\
    'dict')
    #创建套接字
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#解决端口占用
    s.bind(ADDR)
    s.listen(5)
    #处理僵尸
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)#***
    while True:
        try:
            c,addr=s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        #创建父进程
        pid=os.fork()
        if pid==0:
            s.close()
            do_child(c,db)#子进程函数
            sys.exit(0)
        else:
            c.close()
def do_child(c,db):
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            c.close()
            sys.exit()
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_history(c,db,data)
        
#注册
def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name ='%s'"%name
    cursor.execute(sql)
    print(sql)

    result = cursor.fetchone()

    if result != None:
        c.send(b'EXISTS')
        return
    
    #插入用户
    sql = "insert into user (name,passwd) values\
    ('%s','%s')"%(name,passwd)
    print(sql)
    try:
        cursor.execute(sql)
        db.commit() 
        c.send(b'OK')
    except Exception:
        cd.rollback()
        c.send(b'FAIL')
    else:
        print("%s注册成功"%name)


def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()

    sql = "select * from user where name = '%s' and passwd ='%s'"%(name,passwd)
    #查找用户
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        c.send(b'FAIL')
    else:
        c.send(b'OK')
        print("%s登录成功"%name)

def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    
    #内部函数可以直接使用外部函数变量
    def insert_history():
        cursor = db.cursor()
        tm = time.ctime()
        sql="insert into hist (name,word,time)values('%s','%s','%s')"%(name,word,tm)
        #插入历史记录
        try:
            cursor.execute(sql)#执行sql语句
            db.commit()#同步到数据库
            # print('sql执行')
        except Exception as e:
            print(e)
            db.rollback()#执行错误，退回之前的结果
            # print('sql未执行')
            print(sql)
        
        cursor.close()
    #使用单词本查找
    try:
        f = open(DICT_TEXT,'rb')
    except:
        c.send("服务器异常".encode())
        return
    while True:
        line = f.readline().decode()
        w = line.split(' ')[0]
        if (not line) or w > word:
            c.send("FAIL".encode())
            return
        elif w == word:
            time.sleep(0.1)
            c.send(line.encode())
            insert_history()
            # print('插入信息')
            return
    f.close()

def do_history(c,db,data):
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()

    sql = "select * from hist where name =%s"%name
    cursor.execute(sql)
    result = cursor.fetchall()
    if not result:
        c.send(b'FAIL')
        return
    else:
        c.send(b'OK')
        time.sleep(0.1)

    #发送历史记录
    for i in result:
        msg = "%4s    %4s    %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
        time.sleep(0.1)
    c.send(b'##')




            

if __name__ == '__main__':
    main()