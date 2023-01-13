import sys
import time
import serial
import multiprocessing
# from concurrent.futures import ProcessPoolExecutor
import numpy as np
from matplotlib import pyplot as plt

sys.path.append('./script')
import calc_angle

# imu_data=np.zeros(3)

def read_imu(imu_data):
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
            imu_data[0],imu_data[1],imu_data[2]=imu.GetSensorData(recv_data,False)

def zero_calib(imu_data,calib_data):

    roll=[]
    pitch=[]
    for i in range(100):
        roll.append(float(imu_data[1]))
        pitch.append(float(imu_data[2]))
        print(roll[i])
        time.sleep(0.01)
        
    calib_data[0] = np.mean(roll)
    calib_data[1] = np.mean(pitch)
    print(calib_data[0],calib_data[1])


def plot_imu(imu_data,calib_data):
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
        t = np.append(t, float(imu_data[0]))
        t = np.delete(t, 0)
        roll = np.append(roll, float(imu_data[1])-calib_data[0])
        roll = np.delete(roll, 0)
        pitch = np.append(pitch , float(imu_data[2])-calib_data[1])
        pitch = np.delete(pitch , 0)
        li_roll.set_xdata(t)
        li_roll.set_ydata(roll)     
        li_roll.set_label("roll")      
        li_pitch.set_xdata(t)
        li_pitch.set_ydata(pitch)           
        li.set_xdata(t)
        li.set_ydata(r)           
        plt.xlim(min(t), max(t))
        plt.ylim(min(min(roll),min(pitch))-5, max(max(roll),max(pitch))+5)
        # plt.ylim(-30, 30)

        # print("roll pitch:"+str(float(imu_data[1])-calib_data[0])+str(float(imu_data[2])-calib_data[1]))
        # print("\033[1A",end="")

        plt.pause(0.01)

if __name__ == '__main__':

    calib_data = multiprocessing.Array('d', 2) 
    imu_data = multiprocessing.Array('d', 3)
    
    try:
        # p1 = multiprocessing.Process(name="p1", target=read_imu)
        # p2 = multiprocessing.Process(name="p2", target=plot_imu)
        p1 = multiprocessing.Process(name="p1", target=read_imu, args=(imu_data,),daemon=False)
        p2 = multiprocessing.Process(name="p2", target=plot_imu, args=(imu_data,calib_data),daemon=False)
        # p3 = multiprocessing.Process(name="p3", target=zero_calib, args=(imu_data,calib_data),daemon=False)

        p1.start()
        p2.start()
        # p3.start()

        while True :
            input()
            zero_calib(imu_data,calib_data)

        
    

    except KeyboardInterrupt:
        sys.exit()