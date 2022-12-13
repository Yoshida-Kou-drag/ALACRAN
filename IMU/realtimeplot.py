import sys
import serial
import multiprocessing
# from concurrent.futures import ProcessPoolExecutor
import numpy as np
from matplotlib import pyplot as plt

sys.path.append('./script')
import calc_angle

# imu_data=np.zeros(3)

def read_imu(q):
    imu = calc_angle.IMU()
    ser = serial.Serial(
        # port = "/dev/ttyACM0",  #Linux
        port = 'COM3',            #Windows
        baudrate = 57600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        stopbits = serial.STOPBITS_ONE,
        )
    
    while(True) :
        if ser.in_waiting > 0:
            # print('in_waiting is',ser.in_waiting)
            recv_data = ser.read(28)
            imu_data=imu.GetSensorData(recv_data,True)
            q.put(imu_data)

def plot_imu(q):
    # global imu_data
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

    while(1):
        while q.qsize():
            imu_data=q.get()
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

if __name__ == '__main__':

    q = multiprocessing.Queue(maxsize=1)
    
    try:
        # p1 = multiprocessing.Process(name="p1", target=read_imu)
        # p2 = multiprocessing.Process(name="p2", target=plot_imu)
        p1 = multiprocessing.Process(name="p1", target=read_imu, args=(q,),daemon=False)
        p2 = multiprocessing.Process(name="p2", target=plot_imu, args=(q,),daemon=False)

        p1.start()
        p2.start()
        
    

    except KeyboardInterrupt:
        sys.exit()