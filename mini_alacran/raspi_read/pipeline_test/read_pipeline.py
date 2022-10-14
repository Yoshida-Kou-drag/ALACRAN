import os
import sys
import select
import numpy as np
import time
from matplotlib import pyplot as plt

IPC_FIFO_NAME_READ = "imu_pipe"

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


#plot init 
t = np.zeros(100)
y = np.zeros(100)
r = np.zeros(100)

plt.ion()
plt.figure()
li, = plt.plot(t, y)
li2, = plt.plot(t, r)
# plt.ylim(0, 5)
plt.xlabel("time[s]")
plt.ylabel("angle")

while True: #web->STM
        try:      
            print("pooling")
            if (fifo_read, select.POLLIN) in poll.poll(1000):  # Poll every 1 sec
                print("received web")
                msg = os.read(fifo_read, 25)                   # Read from Pipe A
                msg = msg.decode("utf-8")
                imu_data = msg.split(',')
                # print("read node",msg)
                print("read node",imu_data[0])

                t = np.append(t, float(imu_data[0]))
                t = np.delete(t, 0)
                y = np.append(y, float(imu_data[1]))
                y = np.delete(y, 0)
                li.set_xdata(t)
                li.set_ydata(y)           
                li2.set_xdata(t)
                li2.set_ydata(r)           
                plt.xlim(min(t), max(t))
                plt.ylim(min(y)-5, max(y)+5)

                plt.pause(0.01)

        except KeyboardInterrupt:
            print("keybord interrupt main")
            os.remove(IPC_FIFO_NAME_READ)
            sys.exit(0)
            break
