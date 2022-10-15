import os
import sys
import select

IPC_FIFO_NAME_READ = "testpipe"

#creat read pipeline
if not os.path.exists(IPC_FIFO_NAME_READ):
    os.mkfifo(IPC_FIFO_NAME_READ)  # Create Pipe to Read
else:
    #clears the pipe
    os.system("rm " + IPC_FIFO_NAME_READ)
    os.mkfifo(IPC_FIFO_NAME_READ)  # Create Pipe to Read

fifo_read = os.open(IPC_FIFO_NAME_READ, os.O_RDONLY | os.O_NONBLOCK)  # pipe is opened as read only and in a non-blocking mode
print('Pipe node_ext ready')

poll = select.poll()
poll.register(fifo_read, select.POLLIN)

while True: #web->STM
        try:      
            print("pooling")
            if (fifo_read, select.POLLIN) in poll.poll(1000):  # Poll every 1 sec
                msg = os.read(fifo_read, 10)                   # Read from Pipe A
                msg = msg.decode("utf-8")
                # print("read node",msg)
                print("read node",int(msg))

        except KeyboardInterrupt:
            print("keybord interrupt")
            os.remove(IPC_FIFO_NAME_READ)
            sys.exit(0)
            break