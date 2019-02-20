import os
from time import sleep

pid = os.fork()

if pid < 0:
    print("Error")
elif pid == 0:
    sleep(3)
    print("Child %d process exit"%os.getpid())
    os._exit(3)
else:
    pid,status = os.wait()
    print("pid:",pid)
    #显示子进程原本退出状态
    print('status:',os.WEXITSTATUS(status))
    while True:
        pass
