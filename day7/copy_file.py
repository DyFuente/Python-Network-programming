#父子进程共同复制一个文件,分别复制文件的上半部分和下半部分到另一个新文件中
from multiprocessing import Process 
import os

filename = './test.jpg'
#获取文件大小
size = os.path.getsize(filename)

#复制上半部分
def top():
    f = open(filename,'rb')
    n = size // 2
    fw = open('half_top.jpg','wb')
    while True:
        if n < 1024:
            data = f.read(n)
            fw.write(data)
            break
        else:
            data = f.read(1024)
            fw.write(data)
            n -= 1024
    f.close()
    fw.close()

#复制下半部分
def boot():
    f = open(filename,'rb')
    n = size // 2
    fw = open('half_bottom.jpg','wb')
    f.seek(n,0)
    while True:
        data = f.read(1024)
        if not data:
            break
        fw.write(data)
    f.close()
    fw.close()


p = Process(target=top)
p.start()
boot()
p.join()
print('OK')