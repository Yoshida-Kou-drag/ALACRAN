import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('robot_data.csv', names=['num1', 'num2','num3'])
df = pd.read_csv('robot_data.csv', names=['num1', 'num2','num3','num4','num5'])
plt.figure()
plt.plot(df['num1'],df['num2'],label='roll')
plt.plot(df['num1'],df['num3'],label= "pich")
plt.plot(df['num1'],df['num4'],label= "left_deg")
plt.plot(df['num1'],df['num5'],label= "right_deg")
# plt.plot(range(0,count),df['num1'],marker="o",markersize=2)
plt.show()