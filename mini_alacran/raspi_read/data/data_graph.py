import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# df = pd.read_csv('robot_data.csv', names=['num1', 'num2','num3'])
df = pd.read_csv('robot_data_1642968176.97497.csv', names=['num1', 'num2','num3','num4','num5','num6'])
# roll = np.array(df['num2'])
# print(roll[0])
# pitch = np.array(df['num3'])
# ptop_deg = []
# file = open("ptop_data.csv","w")

# for i in range(len(roll)) :
#     ptop_deg.append(math.degrees(math.atan2(roll[i], pitch[i])))
#     # file.write(str(df['num1'][i]) + "," + str(ptop_deg[i]) + "\n") 
#     file.write(str(df['num1'][i]) + "," + str(df['num2'][i]) + "," + str(df['num3'][i]) + "," + str(df['num4'][i]) + "," + str(df['num5'][i]) + "," + str(ptop_deg[i]) + "\n") 

plt.figure()
plt.plot(df['num1'],df['num2'],label='roll')
plt.plot(df['num1'],df['num3'],label= "pich")
plt.plot(df['num1'],df['num4'],label= "left_deg")
plt.plot(df['num1'],df['num5'],label= "right_deg")
plt.plot(df['num1'],df['num6'],label= "ptop_deg")
# plt.plot(range(0,count),df['num1'],marker="o",markersize=2)
plt.legend()
plt.show()

# file.close()