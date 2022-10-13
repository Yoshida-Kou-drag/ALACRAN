import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import math
import calc_angle

imu =  calc_angle.IMU()

#initialize serial port
ser = serial.Serial(
    # port = "/dev/ttyACM0",  #Linux
    port = 'COM6',            #Windows
    baudrate = 57600,
    parity = serial.PARITY_NONE,
    bytesize = serial.EIGHTBITS,
    stopbits = serial.STOPBITS_ONE,
    )

if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here
rs = [] #for theoretical probability

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    #Aquire and parse data from serial port
    # line=ser.readline()      #ascii
    # line_as_list = line.split(b',')
    # i = int(line_as_list[0])
    # relProb = line_as_list[1]
    # relProb_as_list = relProb.split(b'\n')
    # relProb_float = float(relProb_as_list[0])
	
	# Add x and y to lists
    if ser.in_waiting > 0:
        # print('in_waiting is',ser.in_waiting)
        recv_data = ser.read(28)    
        imu_data = imu.GetSensorData(recv_data,False)
        xs.append(i)
        ys.append(imu_data[1])
        rs.append(0.5)

    # Limit x and y lists to 20 items
    #xs = xs[-20:]
    #ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Experimental Probability")
    ax.plot(xs, rs, label="Theoretical Probability")
    # plt.xlim(-30,30)
    plt.ylim(-30,30)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('This is how I roll...')
    plt.ylabel('Relative frequency')
    plt.legend()
    # plt.axis([1, None, 0, 1.1]) #Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo

# Set up plot to call animate() function periodically
try:
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10)
    plt.show()

except KeyboardInterrupt:
    ser.close()