from threading import Thread
from time import sleep

#含有参数的线程函数
def fun(sec,name):
    print('线程函数传参')
    sleep(sec)
    print("%s 执行完毕"%name)

#创建多个线程
threads = []
for i in range(5):
    t = Thread(target=fun,args=(2,),kwargs={'name':'认真%d拳'%(i+1)})
    threads.append(t)
    t.start()

for i in threads:
    i.join() 