import os
import serial
import struct
import calc_angle 

#############init#######################
IPC_FIFO_NAME_READ = "imu_pipe"

if not os.path.exists(IPC_FIFO_NAME_READ):
    os.mkfifo(IPC_FIFO_NAME_READ)  # Create Pipe to Read
else:
    #clears the pipe
    os.system("rm " + IPC_FIFO_NAME_READ)
    os.mkfifo(IPC_FIFO_NAME_READ)  # Create Pipe to Read

while not os.path.exists(IPC_FIFO_NAME_READ):
    pass

fifo_write = os.open(IPC_FIFO_NAME_READ, os.O_WRONLY | os.O_NONBLOCK)  # pipe is opened as read only and in a non-blocking mode
print('Pipe node_ext ready')

imu =  calc_angle.IMU()
ser = serial.Serial(
    port = "/dev/ttyACM0",  #Linux
    # port = 'COM6',            #Windows
    baudrate = 57600,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    )

while(True) :
    try:
        if ser.in_waiting > 0:
            print('in_waiting is',ser.in_waiting)
            recv_data = ser.read(28)
            imu_data = imu.GetSensorData(recv_data)
            os.write(fifo_write, b'\xcd\xcc\xf6B')
            
    except KeyboardInterrupt:
        os.remove(IPC_FIFO_NAME_READ)

    except Exception as e:
        os.remove(IPC_FIFO_NAME_READ)
        print(e)
        break
