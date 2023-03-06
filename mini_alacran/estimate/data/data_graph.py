import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('robot_data.csv', names=['num1', 'num2','num3'])
df = pd.read_csv('test1.csv', names=['num1', 'num2','num3','num4','num5','num6'])
plt.figure()
ax = plt.axes()
plt.minorticks_on()
ax.grid(which="major",alpha=0.6)
ax.grid(which="minor",alpha=0.3)

plt.plot(df['num1'],df['num2'],label='roll')
plt.plot(df['num1'],df['num3'],label= "pich")
plt.plot(df['num1'],df['num4'],label= "left_deg")
plt.plot(df['num1'],df['num5'],label= "right_deg")
plt.legend()
# plt.plot(range(0,count),df['num1'],marker="o",markersize=2)
plt.show()