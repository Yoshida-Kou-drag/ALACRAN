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
roll = np.zeros(100)
pitch =np.zeros(100)

r = np.zeros(100)

plt.ion()
plt.figure()
li_roll, = plt.plot(t, roll,label='roll')
li_pitch, = plt.plot(t, pitch,label='pitch')
li, = plt.plot(t, r)
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
                roll = np.append(roll, float(imu_data[1]))
                roll = np.delete(roll, 0)
                pitch = np.append(pitch , float(imu_data[2]))
                pitch = np.delete(pitch , 0)
                li_roll.set_xdata(t)
                li_roll.set_ydata(roll)     
                li_roll.set_label("roll")      
                li_pitch.set_xdata(t)
                li_pitch.set_ydata(pitch)           
                li.set_xdata(t)
                li.set_ydata(r)           
                plt.xlim(min(t), max(t))
                plt.ylim(-30, 30)

                plt.pause(0.01)

        except KeyboardInterrupt:
            print("keybord interrupt main")
            os.remove(IPC_FIFO_NAME_READ)
            sys.exit(0)
            break
