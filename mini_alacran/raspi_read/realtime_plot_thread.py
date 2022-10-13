import serial
import threading
import numpy as np
import time
from matplotlib import pyplot as plt
import calc_angle
import math

imu =  calc_angle.IMU()

ser = serial.Serial(
    # port = "/dev/ttyACM0",  #Linux
    port = 'COM6',            #Windows
    baudrate = 57600,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    )


    

pretime = 0.0


# ser.write("*".encode())
# data = ser.readline().strip().rsplit()
# tInt = float(data[0])

def read_posture():
    global imu_data
    while True:
        if ser.in_waiting > 0:
            # print('in_waiting is',ser.in_waiting)
            recv_data = ser.read(28)    
            imu_data = imu.GetSensorData(recv_data,False)
            # print(ptop_deg)

def compute_fps():
    global pretime
    curtime = time.time()
    time_diff = curtime - pretime
    fps = 1.0 / (time_diff + 1e-16)
    pretime = curtime

    return fps 

def realtime_plot():
    global imu_data
    t = np.zeros(10)
    y = np.zeros(10)

    plt.ion()
    plt.figure()
    li, = plt.plot(t, y)
    # plt.ylim(0, 5)
    plt.xlabel("time[s]")
    plt.ylabel("angle")
    
    while True:
    # 配列をキューと見たてて要素を追加・削除
        t = np.append(t, imu_data[0])
        t = np.delete(t, 0)
        y = np.append(y, imu_data[1])
        y = np.delete(y, 0)
        li.set_xdata(t)
        li.set_ydata(y)           
        plt.xlim(min(t), max(t))
        plt.ylim(-45, 45)

        fps = compute_fps()
        plt.title(f"fps: {fps:0.1f} Hz")
        plt.pause(0.01)

thread1 = threading.Thread(target=read_posture)
thread2 = threading.Thread(target=realtime_plot)
thread1.setDaemon(True)
thread2.setDaemon(True)
thread1.start()
thread2.start()

try:
    while True:    
        pass

except KeyboardInterrupt:
    ser.close()