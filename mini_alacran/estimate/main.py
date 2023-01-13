import sys
import serial
import pigpio
import time
import math
import numpy as np
import multiprocessing

sys.path.append('./script/')
import estimate_2D_plot 
import calc_angle

def read_imu(imu_data):
    imu = calc_angle.IMU()
    ser = serial.Serial(
        port = "/dev/ttyACM0",  #Linux
        # port = 'COM3',            #Windows
        baudrate = 57600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        stopbits = serial.STOPBITS_ONE,
        )
    
    print("start imu reading")
    while(True) :
        if ser.in_waiting > 0:
            # print('in_waiting is',ser.in_waiting)
            recv_data = ser.read(28)
            imu_data[0],imu_data[1],imu_data[2]=imu.GetSensorData(recv_data,False)
            # ptop_deg = math.degrees(math.atan2(imu_data[1], imu_data[2]))

def get_sensor_avg(imu_data,calib_data):
    roll=[]
    pitch=[]
    for i in range(100):
        roll.append(float(imu_data[1]-calib_data[0]))
        pitch.append(float(imu_data[2]-calib_data[1]))
        time.sleep(0.01)
    filter_roll = np.mean(roll)
    filter_pitch = np.mean(pitch)
    print("filter data is",filter_roll,filter_pitch)
    ptop_deg = -math.degrees(math.atan2(filter_roll, filter_pitch))
    
    return ptop_deg,filter_pitch


def zero_calib(imu_data,calib_data):

    roll=[]
    pitch=[]
    for i in range(100):
        roll.append(float(imu_data[1]))
        pitch.append(float(imu_data[2]))
        time.sleep(0.01)
    calib_data[0] = np.mean(roll)
    calib_data[1] = np.mean(pitch)
    print("calib data is",calib_data[0],calib_data[1])

def deg_to_duty(degree):
    dc = 2.0 + (11.0-2.0)/180*(degree+90)
    return dc

def servo_moving(imu_data,calib_data):
    gpio_pin0 = 18 #right
    gpio_pin1 = 19 #left

    pi = pigpio.pi()
    pi.set_mode(gpio_pin0, pigpio.OUTPUT)
    
    left_deg_input =0
    right_deg_input = 0

    pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(21)*10000))
    pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(15)*10000))
    time.sleep(1)
    zero_calib(imu_data,calib_data)

    for i in range(1):
        # print("input Degree : ")
        # left_deg_input, right_deg_input=input().split()
        # left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        
        left_deg_input, right_deg_input=5, 0
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)
        right_tilt,left_pitch = get_sensor_avg(imu_data,calib_data)

        left_deg_input, right_deg_input=0, 0
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)

        left_deg_input, right_deg_input=0, 5
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)
        left_tilt,right_pitch = get_sensor_avg(imu_data,calib_data)

        left_deg_input, right_deg_input=0, 0
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)

    return left_tilt,right_tilt,left_pitch,right_pitch
    

if __name__ == "__main__":
    calib_data = multiprocessing.Array('d', 2) 
    imu_data = multiprocessing.Array('d', 3)
    # filter_imu = multiprocessing.Array('d', 3)

    try :
        p1 = multiprocessing.Process(name="p1", target=read_imu, args=(imu_data,),daemon=False)

        p1.start()

        while True:
            input()
            print("starting!")
            left_tilt,right_tilt,left_pitch,right_pitch = servo_moving(imu_data,calib_data)
            print(left_tilt,right_tilt,left_pitch,right_pitch)
            estimate_2D_plot.estimate_main(left_tilt,right_tilt,left_pitch,right_pitch)
    
    except KeyboardInterrupt:
        sys.exit()