import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import numpy as np
import sys

sys.path.append('./script/')
from rotation_matrix import RotationMatrix
from plot_ground_test import EstimateGround
from mesh_adj import MeshAdj

def setting_graph(ax):
    xmin,xmax = -150,150
    ymin,ymax = -150,150
    plt.minorticks_on()
    ax.grid(which="major",alpha=0.6)
    ax.grid(which="minor",alpha=0.3)
    plt.hlines([0], xmin, xmax, "blue", linestyles='dashed')     # hlines
    plt.axis('scaled')
    ax.set_aspect('equal')
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

def alacran_model(ax):
    body = patches.Rectangle(xy=(-69, -128), width=138, height=150, ec='#000000', fill=False)
    left_arm = patches.Rectangle(xy=(-90, -20), width=13.2, height=126, ec='#000000', fill=False)
    right_arm = patches.Rectangle(xy=(76.8, -20), width=13.2, height=126, ec='#000000', fill=False)
    plt.plot(0, -36, marker='o', markersize=10, color='#000000') #　円
    ax.add_patch(body)
    ax.add_patch(left_arm)
    ax.add_patch(right_arm)

def ground_point(debug=True):
    la_ground=[-83.4, 70]
    ra_ground=[83.4, 20]
    body_ground = [-16.6,-80]
    tilt_la_to_body = (la_ground[1]-body_ground[1])/(la_ground[0]-body_ground[0])
    tilt_ra_to_body = (ra_ground[1]-body_ground[1])/(ra_ground[0]-body_ground[0])
    if debug:
        print("Tilt",math.degrees(math.atan(tilt_la_to_body)),math.degrees(math.atan(tilt_ra_to_body)))

    plt.plot([la_ground[0],body_ground[0]], [la_ground[1],body_ground[1]],color="red",alpha=0.5)
    plt.plot([ra_ground[0],body_ground[0]], [ra_ground[1],body_ground[1]],color="red",alpha=0.5)
    plt.plot(la_ground[0],la_ground[1], marker='o', markersize=20, color='blue', alpha = 0.5) #　円
    plt.plot(ra_ground[0], ra_ground[1], marker='o', markersize=20, color='blue', alpha = 0.5) #　円
    plt.plot(body_ground[0], body_ground[1], marker='o', markersize=20, color='blue', alpha = 0.5) #　円


def init_line():

    left_arm_range = np.array([[-83.4 ,0] ,[-83.4 ,88.5]]) 
    
    right_arm_range =np.array([[83.4,0] ,[83.4,88.5]]) 

    body_range =np.array([[0,-36.],
                        [-69. ,-65.78417266],
                        [-69. ,-109.25 ],
                        [69 ,-109.25 ],
                        [69 ,-65.78417266]]) 
    
    plt.plot(left_arm_range[:,:1], left_arm_range[:,1:2],color="green",alpha=0.5)
    plt.plot(right_arm_range[:,:1], right_arm_range[:,1:3],color="green",alpha=0.5)
    patch = patches.Polygon(xy=body_range[:,:2], closed=True,alpha=0.5)
    ax.add_patch(patch)
    print("left_arm_range",left_arm_range[:,:1], left_arm_range[:,1:3])
    print("right_arm_range",right_arm_range[:,:1], right_arm_range[:,1:3])
    print("body ",body_range[:,:2])

def estimate_plot(left_arm_range,right_arm_range,body_range,gp):
    plt.plot(left_arm_range[0], left_arm_range[1],linewidth=4,color="red")
    plt.plot(right_arm_range[0], right_arm_range[1],linewidth=4,color="red")
    patch = patches.Polygon(xy=body_range[:,:2], closed=True)
    ax.add_patch(patch) 

if __name__ == "__main__":
    fig = plt.figure(figsize=[8,8])
    ax = plt.axes()
    setting_graph(ax)

    estimate_ground = EstimateGround()
    left_arm_range,right_arm_range,body_range,gp = estimate_ground.get_ground_range()
    ####################### 計算後##############################
    estimate_ground.right_tilt_range(45)
    estimate_ground.left_arm_estimate(10,  4.665821)
    # estimate_ground.left_tilt_range(-65.99499623269556)
    # estimate_ground.right_arm_estimate(10, 2)
    
    left_arm_range,right_arm_range,body_range,gp = estimate_ground.get_ground_range()
    

    alacran_model(ax)
    ground_point()
    init_line()
    estimate_plot(left_arm_range,right_arm_range,body_range,gp)
    
    plt.show()