from multiprocessing import Pool 
from time import sleep,ctime

def fun(n):
    sleep(1)
    return n * n

#创建进程池
pool = Pool()

#使用map将事件放入进程池
r = pool.map(fun,[1,2,3,4,5])

pool.close()
pool.join()
print("结果:",r)