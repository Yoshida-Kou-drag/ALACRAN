import math

x1 = 31.29310979
y1 = -76.0084293

x2 = 44.05064531
y2 = -86.46735191
a = (y1-y2)/(x1-x2)

b = y1-a*x1

print(a,b)

ten = [35,-80]

kyori = abs(a*ten[0]-ten[1]+b)/math.sqrt(a**2+1)

print("kyori :",kyori)