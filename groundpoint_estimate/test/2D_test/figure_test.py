import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def setting_graph(ax):
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

def line():

    left_arm_range = np.array([[-83.4 ,0] ,[-83.4 ,88.5]]) 
    
    right_arm_range =np.array([[83.4,0] ,[83.4,88.5]]) 

    body_range =np.array([[0,-36.],
                        [-69. ,-65.78417266],
                        [-69. ,-109.25 ],
                        [69 ,-109.25 ],
                        [69 ,-65.78417266]]) 
    
    plt.plot(left_arm_range[:,:1], left_arm_range[:,1:2],color="green")
    plt.plot(right_arm_range[:,:1], right_arm_range[:,1:3],color="green")
    patch = patches.Polygon(xy=body_range[:,:2], closed=True)
    ax.add_patch(patch)
    print("left_arm_range",left_arm_range[:,:1], left_arm_range[:,1:3])
    print("right_arm_range",right_arm_range[:,:1], right_arm_range[:,1:3])
    print("body ",body_range[:,:2])


if __name__ == "__main__":
    fig = plt.figure(figsize=[8,8])
    ax = plt.axes()
    xmin,xmax = -150,150
    ymin,ymax = -150,150
    
    setting_graph(ax)
    alacran_model(ax)
    line()
    
    plt.show()