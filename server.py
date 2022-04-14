import os
from multiprocessing import Process

def webserver():
    os.system("python3 ./webserver.py")     
def ssh():
    os.system("python ./ssh.py") 

if __name__ == '__main__':
    p = Process(target=webserver)
    q = Process(target=ssh)
    p.start()
    q.start()
    p.join()
    q.join()
