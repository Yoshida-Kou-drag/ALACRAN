from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

import math

ax = plt.figure().add_subplot(111, projection='3d')

my_chain = Chain.from_urdf_file("alacran_robotarm.URDF")

i=0
while True:
    for i in range (10):
        axis_y = -i*0.05-0.1
        my_chain.plot(my_chain.inverse_kinematics([0, axis_y, 0.2]), ax)

        ax.auto_scale_xyz([-0.5,0.5], [-0.5,0.5], [0,1])
        plt.pause(0.1)
        ax.cla()
    
    for i in range (10):
        axis_x = -i*0.04+0.2
        my_chain.plot(my_chain.inverse_kinematics([axis_x, axis_y, 0.2]), ax)

        ax.auto_scale_xyz([-0.5,0.5], [-0.5,0.5], [0,1])
        plt.pause(0.1)
        ax.cla()

    for i in range (10):
        axis_z = i*0.04
        my_chain.plot(my_chain.inverse_kinematics([axis_x, axis_y, 0.2+axis_z]), ax)

        ax.auto_scale_xyz([-0.5,0.5], [-0.5,0.5], [0,1])
        plt.pause(0.1)
        ax.cla()
    
    # for i in range(3):
    #     if i == 0:
    #         my_chain.plot(my_chain.inverse_kinematics([0, -0.1, 0.2]), ax)
    #     elif i == 1:
    #         my_chain.plot(my_chain.inverse_kinematics([0, -0.2, 0.2]), ax)
    #     elif i == 2:
    #         my_chain.plot(my_chain.inverse_kinematics([0, -0.3, 0.2]), ax)

        