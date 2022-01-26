import ikpy
import numpy as np
import time
import b3mCtrl
# import ikpy.utils.plot as plot_utils
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

# my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.URDF")
my_chain = ikpy.chain.Chain.from_urdf_file("todoroki_robotarm.urdf")

aaa = b3mCtrl.B3mClass()
aaa.begin("/dev/ttyUSB0",1500000)
idx = [1,2,3,4,5,6,7,8,9]
print (aaa.setTrajectoryType(255,"EVEN"))
print (aaa.setMode(255,"POSITION"))
# robot_arm.begin("/dev/ttyUSB0",1500000)

pos = [0]*6

home_pos = my_chain.forward_kinematics([0] * 5)[:,3][0:3]
print("forward_kinematics", home_pos)
home_pos = my_chain.forward_kinematics([0,1.8,1.8,0,0])#[:,3][0:3]
print("forward_kinematics", home_pos)
# my_chain.inverse_kinematics([2, 2, 2])
my_chain.plot(my_chain.inverse_kinematics(home_pos), ax)
# my_chain.plot(my_chain.inverse_kinematics([0.2,0.2,0.2]), ax)
# my_chain.plot(my_chain.inverse_kinematics([0.0,0.5,0.2]), ax)
my_chain.plot(my_chain.inverse_kinematics([
    [1, 0, 0, 0.2],
    [0, 1, 0, 0.5],
    [0, 0, 1, 0.2],
    [0, 0, 0, 1]
    ]),ax)


# for i in range(-4,5):
#     x = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([x, 0.5, 0.5]), ax)

# for i in range(-4,5):
#     y = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([0, y, 0.5]), ax)

# for i in range(0,10):
#     z = i * 0.1
#     my_chain.plot(my_chain.inverse_kinematics([0, 0.5, z]), ax)
# my_chain.plot(my_chain.inverse_kinematics([0.7, 0.2, 0.2]), ax)
# print(my_chain.inverse_kinematics(home_pos))
# print(my_chain.inverse_kinematics([0.2,0.2,0.2]))
# print(my_chain.inverse_kinematics([0.0,0.5,0.2]))

rad = my_chain.inverse_kinematics([
    [1, 0, 0, 0.2],
    [0, 1, 0, 0.5],
    [0, 0, 1, 0.2],
    [0, 0, 0, 1]
    ])

print("rad : ",rad)

print("enter move arm")
input()
for i in range(len(rad)):
    rad[i] = rad[i].item()
    rad[i] =  round(rad[i],3)
    
    if i == 0:
        pos[i+1]=aaa.radToPos(rad[i])

    elif i == 1:
        pos[2]=aaa.radToPos(rad[i])
        pos[3]=-aaa.radToPos(rad[i])
    
    elif i == 2 or i == 3:
        pos[i+2]=aaa.radToPos(rad[i])-9000
    
    print (aaa.positionCmd(i,pos[i],5))

        
print("rad : ",rad)
print("pos = ",pos )

matplotlib.pyplot.show()
