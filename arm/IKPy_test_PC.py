import ikpy.chain
import numpy as np
import math
import b3mCtrl
import time
# import ikpy.utils.plot as plot_utils
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.URDF")
# my_chain = ikpy.chain.Chain.from_urdf_file("./todoroki_robotarm.urdf")

idx = [1,2,3,4,5]
count =0
pos = [0]*10
x,y,z = 0,0.2,0.5

#################b3m setup##########################
aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)
idx = [1,2,3,4,5]
print (aaa.setTrajectoryType(255,"EVEN"))
print (aaa.setMode(255,"POSITION"))

pos = [0]*5

home_pos = my_chain.forward_kinematics([0,0,math.radians(-60),math.radians(-120),0])[:,3][0:3]
b3m_calibdata = [0,0,aaa.radToPos(math.radians(-60)),aaa.radToPos(math.radians(-120)),0]
print("calib data is ",b3m_calibdata)

# my_chain.plot(my_chain.inverse_kinematics(home_pos), ax)
# my_chain.plot([0,0,math.radians(-60),math.radians(-120),math.radians(30)], ax)
# print(str([x,y,z]) +" : " +  str(my_chain.inverse_kinematics(home_pos)))
# print(str(home_pos))



#Home pos
rad = my_chain.inverse_kinematics(home_pos) 
my_chain.plot(rad, ax)
for i in range(len(rad)):
    rad[i] = rad[i].item()
    rad[i] =  round(rad[i],3)
    if rad[i]<math.radians(-360) or rad[i] > math.radians(360):
        rad[i] = rad[i]%math.radians(360)
    print("rad is",rad[i])
    pos[i] = aaa.radToPos(rad[i])
    if pos[i] > 18000 :
        pos[i] = pos[i] - 36000
    elif pos[i]<-18000 :
        pos[i] = pos[i] + 36000

    pos[i] = pos[i] - b3m_calibdata[i]

for i in range(len(pos)-1): print(aaa.positionCmd(idx[i],pos[i+1],5))
print (aaa.positionCmd(5,0,5))
time.sleep(5)
print(" pos is ",pos)


#chatch pos
rad = my_chain.inverse_kinematics([0, 0.1, 0.3]) 
my_chain.plot(rad, ax)
for i in range(len(rad)):
    rad[i] = rad[i].item()
    rad[i] =  round(rad[i],3)
    if rad[i]<math.radians(-360) or rad[i] > math.radians(360):
        rad[i] = rad[i]%math.radians(360)
    print("rad is",rad[i])
    pos[i] = aaa.radToPos(rad[i])
    if pos[i] > 18000 :
        pos[i] = pos[i] - 36000
    elif pos[i]<-18000 :
        pos[i] = pos[i] + 36000

    pos[i] = pos[i] - b3m_calibdata[i]

pos[4] = 9000
for i in range(len(pos)-1): print(aaa.positionCmd(idx[i],pos[i+1],5))
time.sleep(5)
print(" pos is ",pos)

# catch
print (aaa.positionCmd(5,3000,5))


# move up
rad = my_chain.inverse_kinematics([0, 0.1, 0.5]) 
rad[2] = rad[2]-rad[3]
rad[3] = -rad[3]
my_chain.plot(rad, ax)
for i in range(len(rad)):
    rad[i] = rad[i].item()
    rad[i] =  round(rad[i],3)
    if rad[i]<math.radians(-360) or rad[i] > math.radians(360):
        rad[i] = rad[i]%math.radians(360)
    print("rad is",rad[i])
    pos[i] = aaa.radToPos(rad[i])
    if pos[i] > 18000 :
        pos[i] = pos[i] - 36000
    elif pos[i]<-18000 :
        pos[i] = pos[i] + 36000

    pos[i] = pos[i] - b3m_calibdata[i]

pos[4] = 0
for i in range(len(pos)-1): print(aaa.positionCmd(idx[i],pos[i+1],5))
time.sleep(5)
print(" pos is ",pos)

# release pos
rad = my_chain.inverse_kinematics([0.1, 0.1, 0.3]) 
my_chain.plot(rad, ax)
for i in range(len(rad)):
    rad[i] = rad[i].item()
    rad[i] =  round(rad[i],3)
    if rad[i]<math.radians(-360) or rad[i] > math.radians(360):
        rad[i] = rad[i]%math.radians(360)
    print("rad is",rad[i])
    pos[i] = aaa.radToPos(rad[i])
    if pos[i] > 18000 :
        pos[i] = pos[i] - 36000
    elif pos[i]<-18000 :
        pos[i] = pos[i] + 36000

    pos[i] = pos[i] - b3m_calibdata[i]

pos[4] = 9000
for i in range(len(pos)-1): print(aaa.positionCmd(idx[i],pos[i+1],5))
time.sleep(5)
print(" pos is ",pos)

#Release
print (aaa.positionCmd(5,0,5))




# for i in [-0.3,-0.2,-0.1,0,0.1,0.2,0.3]:
#     x = i 
#     for j in [0.2,0.3,0.4,0.5,0.6,0.8]:
#         y = j
#         for k in [0.4,0.5 ,0.6]:
#             z = k
#             count+=1
#             my_chain.plot(my_chain.inverse_kinematics([x, y, z]), ax)
#             print(str([x,y,z]) +" : " +  str(my_chain.inverse_kinematics([x, y, z])))

# for i in [-0.25,-0.1,0,0.1,0.25]:
#     x = i 
#     for j in [0.1,0.2,0.4,0.6]:
#         y = j
#         for k in [0.3,0.4]:
#             z = k
#             count+=1
#             my_chain.plot(my_chain.inverse_kinematics([x, y, z]), ax)
#             print(str([x,y,z]) +" : " +  str(my_chain.inverse_kinematics([x, y, z])))

# for i in range(0,10):
#     z = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([0, 0.5, z]), ax)

# my_chain.plot(my_chain.inverse_kinematics([0.7, 0.2, 0.2]), ax)
# print(my_chain.inverse_kinematics(home_pos))
# print(my_chain.inverse_kinematics([0.2,0.2,0.2]))
# print(my_chain.inverse_kinematics([0.0,0.5,0.2]))


# print("rad : ",rad)
ax.auto_scale_xyz([-0.5,0.5], [-0.5,0.5], [0,1])
matplotlib.pyplot.show()
