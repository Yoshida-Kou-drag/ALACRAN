import pigpio
import pandas as pd
import matplotlib.pyplot as plt
import threading
import time
import calc_angle 
import robot
import serial
import math
import sys

imu =  calc_angle.IMU()
robot = robot.Robot(128,107) #robot param is (body length , arm length)
ser = serial.Serial(
    port = "/dev/ttyACM0",  #Linux
    # port = 'COM4',            #Windows
    baudrate = 57600,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    )

gpio_pin0 = 18 #right
gpio_pin1 = 19 #left


pi = pigpio.pi()
pi.set_mode(gpio_pin0, pigpio.OUTPUT)
 
def deg_to_duty(degree):
    dc = 2.0 + (11.0-2.0)/180*(degree+90)
    return dc

def read_posture():
    global imu_data
    while True:
        if ser.in_waiting > 0:
            # print('in_waiting is',ser.in_waiting)
            recv_data = ser.read(28)    
            imu_data = imu.GetSensorData(recv_data,False)
            ptop_deg = math.degrees(math.atan2(imu_data[1], imu_data[2]))
            # print(ptop_deg)

def servo_moving():
    global left_deg_input,right_deg_input
    left_deg_input =0
    right_deg_input = 0
    for i in range(2):
        # print("input Degree : ")
        # left_deg_input, right_deg_input=input().split()
        # left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        
        left_deg_input, right_deg_input=10, 0
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)

        left_deg_input, right_deg_input=0, 0
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)

        left_deg_input, right_deg_input=0, 10
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)

        left_deg_input, right_deg_input=0, 0
        left_deg, right_deg= int(left_deg_input)+15, -int(right_deg_input)+21
        pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(right_deg)*10000))
        pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(left_deg)*10000))
        time.sleep(2)

pi.hardware_PWM(gpio_pin0,50,int(deg_to_duty(21)*10000))
pi.hardware_PWM(gpio_pin1,50,int(deg_to_duty(15)*10000))
time.sleep(2)

thread1 = threading.Thread(target=read_posture)
thread2 = threading.Thread(target=servo_moving)
thread1.start()
thread2.start()

file_name = "./data/robot_data_"+str(time.time())+".csv"
file = open(file_name,"w")

try :
    while True :
        if imu_data[1] < 0.5 and imu_data[2] < 0.5:
            ptop_deg = 0
        else :
            ptop_deg = math.degrees(math.atan2(imu_data[1], imu_data[2]))
        
        file.write(str(imu_data[0]) + "," + str(imu_data[1]) + "," + str(imu_data[2]) + "," + str(left_deg_input) + "," + str(right_deg_input)+ "," + str(ptop_deg)  + "\n") 
        time.sleep(0.1)



 
 
except KeyboardInterrupt:
    file.close()
    pi.set_mode(gpio_pin0,pigpio.INPUT)
    pi.set_mode(gpio_pin1,pigpio.INPUT)
    pi.stop()

    df = pd.read_csv(file_name, names=['num1', 'num2','num3','num4','num5','num6'])
    plt.figure()
    plt.plot(df['num1'],df['num2'],label='roll')
    plt.plot(df['num1'],df['num3'],label= "pich")
    plt.plot(df['num1'],df['num4'],label= "left_deg")
    plt.plot(df['num1'],df['num5'],label= "right_deg")
    plt.plot(df['num1'],df['num6'],label= "ptop deg")
    plt.legend()
    plt.show()
    
    sys.exit()

    # print("estimate deg :",robot.imu_deg_estimator(degree))
