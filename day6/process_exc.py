#父子进程共同复制一个文件,分别复制文件的上半部分和下半部分到另一个新文件中
from multiprocessing import Process 
from time import sleep

f1 = open('day6.txt','rb')
f1.seek(0,2)
file_end = f1.tell()
file_middle = file_end//2
#编写进程函数
def get_upfile():
    try:
        f2 = open('new1.txt','wb')
        f1.seek(0,0)
        up_file = f1.read(file_middle)
        f2.write(up_file)
    except Exception as e:
        print(e)
    finally:
        f2.close()

#创建进程对象
p = Process(target = get_upfile)
#启动进程
p.start()
try:
    f3 = open('new2.txt','wb')
    f1.seek(file_middle,0)
    down_file = f1.read()
    f3.write(down_file)
except Exception as e:
    print(e)
finally:
    f3.close()
#回收进程
p.join()
f1.close()
print('OK')


