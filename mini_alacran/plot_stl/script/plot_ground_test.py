import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from pandas import array

class EstimateGround:
    def __init__(self) :
        self.plot_counter = 0
        
        arm_ground_size = 88.5 #アーム接地長さ
        arm_length = 126 # 実際のアームの長さ
        arm_width = 166.8 # アーム間の距離

        body_ground_size = [138,112.5] # x y 有効範囲
        body_length = 150
        body_width = 138

        gravity_point = [0,0,0] # 重心点
        ax_roll_gp = 36 #回転軸と重心の距離
        body_to_gp = 58 # 重心とbodyの端の距離

        self.left_arm_range = np.array([[-arm_width/2, ax_roll_gp,0],                 # min
                        [-arm_width/2, ax_roll_gp+arm_ground_size,0]])   # max
        
        self.right_arm_range = np.array([[arm_width/2, ax_roll_gp,0],                 # min
                        [arm_width/2, ax_roll_gp+arm_ground_size,0]])    # max

        self.min_deg = [ax_roll_gp/(-arm_width/2),
                   ax_roll_gp/(arm_width/2)]

        self.body_range = np.array([gravity_point,
                     [-body_width/2, self.min_deg[1]*(-body_width/2), 0],
                     [-body_width/2, -(body_length-body_to_gp-(body_length-body_ground_size[1])/2), 0],
                     [body_width/2, -(body_length-body_to_gp-(body_length-body_ground_size[1])/2), 0],
                     [body_width/2,self.min_deg[0]*(body_width/2),0],
                     ])

    # @classmethod
    def get_ground_range(self):
        self.sim_calib = np.array([0, 36, 18 - self.plot_counter])
        self.plot_counter += 1
        body_range = self.body_range - self.sim_calib
        left_arm_range = self.left_arm_range -self.sim_calib
        right_arm_range = self.right_arm_range - self.sim_calib

        return left_arm_range.T,right_arm_range.T,body_range,[0,-36,0]
    
    def right_tilt_range(self,degree): # 右側の傾きから有効範囲を計算
        tilt = math.tan(math.radians(degree))
        print("tilt is ",tilt)
        new_body_range = []

        if tilt*self.right_arm_range[0,0] > self.right_arm_range[1,1] : # 腕の接地点の範囲を超えたら
            b = self.right_arm_range[1,1]-tilt*self.right_arm_range[0,0]
            x = b/(self.min_deg[0]-tilt) 
            y= self.min_deg[0]*x
            new_body_range.append([x,y,0])
        else:
            b=0
            self.right_arm_range[1,1] = tilt*self.right_arm_range[0,0] # アームの有効範囲の更新
            new_body_range.append([0,0,0])
        
        if abs((self.body_range[2,1] - b) / tilt) < abs(self.body_range[2,0]) : # xが限界を超えていなければ
            print("y max",self.body_range[2,1])
            new_body_range.append([(self.body_range[2,0]-b)/tilt, self.body_range[2,1], 0])
        elif abs(self.body_range[1,0]*tilt + b) < abs(self.body_range[2,1]): # yがげんかいをかえてなければ
            print("x max",self.body_range[1,0]*tilt, abs(self.body_range[2,1]))
            new_body_range.append([self.body_range[1,0],self.body_range[1,0]*tilt+b,0])

        b = self.right_arm_range[0,1]-tilt*self.right_arm_range[0,0]
        x = b/(self.min_deg[0]-tilt) 
        y= self.min_deg[0]*x

        print("b is",b)
        print("x is",(self.body_range[2,1] - b) / tilt)

        if abs((self.body_range[2,1] - b) / tilt) < abs(self.body_range[2,0]) : # xが限界を超えていなければ
            new_body_range.append([(self.body_range[2,0]-b)/tilt,self.body_range[2,1],0])
        elif abs(self.body_range[1,0]*tilt + b) < abs(self.body_range[2,1]): # yがげんかいをかえてなければ
            new_body_range.append([self.body_range[1,0],self.body_range[1,0]*tilt+b,0])

        new_body_range.append([x,y,0])

        print("init body range is",self.body_range)
        print("new body range is",new_body_range)
        self.body_range = new_body_range

        return
        

        

