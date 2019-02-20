import os
from time import sleep

print('=============================')
a = 1

pid = os.fork()

if pid < 0:
    print('Create process failed')
elif pid ==0:
    print('Child process')
    print("a = %d"%a)
    a = 10000
else:
    sleep(1)
    print('Parent process')
    print("a:",a)
print('all a=%d'%a)