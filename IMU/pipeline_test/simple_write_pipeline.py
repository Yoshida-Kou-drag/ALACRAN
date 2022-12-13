import os
import sys
import time

IPC_FIFO_NAME_WRITE = "testpipe"
count=0

while True:
    while not os.path.exists(IPC_FIFO_NAME_WRITE):
        pass
    
    try:
        fifo_write = os.open(IPC_FIFO_NAME_WRITE, os.O_WRONLY)
        print("Pipe ext_node ready")
        break
    except:
        # Wait until Pipe B has been initialized
        # print("still trying")
        pass

while(True) :
    try:
        # os.write(fifo_write, count.to_bytes(1,'little'))
        os.write(fifo_write, bytes(format(str(format(count,'010'))), 'utf-8'))
        # os.write(fifo_write, bytes("{0:>10}".format(str(count)), 'utf-8'))
        count+=1
        time.sleep(0.5)
    except KeyboardInterrupt:
        os.close(IPC_FIFO_NAME_WRITE)
        sys.exit(0)