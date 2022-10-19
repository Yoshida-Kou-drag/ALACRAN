from multiprocessing.connection import wait
import os
import sys
import time
import serial
import struct


sys.path.append('..')
import calc_angle

#############init#######################
IPC_FIFO_NAME_WRITE = "imu_pipe"
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
        # os.write(fifo_write, count.to_bytes(1,'little'))
        # os.write(fifo_write, bytes(format(str(format(count,'010'))), 'utf-8'))
        # os.write(fifo_write, bytes("{0:>10}".format(str(count)), 'utf-8'))
        # count-=1
        # time.sleep(0.5)

        if ser.in_waiting > 0:
            print('in_waiting is',ser.in_waiting)
            recv_data = ser.read(28)
            imu_data = imu.GetSensorData(recv_data,False)
            write_data= format(imu_data[0],'.3f') +','
            write_data+= format(imu_data[1],'.3f') +','
            write_data+= format(imu_data[2],'.3f')
            count+=1
            if count > 10:
                os.write(fifo_write, bytes(write_data,'utf-8'))
                count=0
            
    except KeyboardInterrupt:
        os.remove(IPC_FIFO_NAME_WRITE)

    # except Exception as e:
    #     os.remove(IPC_FIFO_NAME_WRITE)
    #     print(e)
    #     break
