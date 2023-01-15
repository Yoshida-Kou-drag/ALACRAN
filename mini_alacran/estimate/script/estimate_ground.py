from cmath import sin
import math
from turtle import radians, tiltangle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from pandas import array
import gift_wrap

class EstimateGround:
    def __init__(self) :
        self.plot_counter = 0
        
        self.arm_ground_size = 88.5 #アーム接地長さ
        arm_length = 126 # 実際のアームの長さ
        arm_width = 166.8 # アーム間の距離

        body_ground_size = [138,112.5] # x y 有効範囲
        body_length = 150
        body_width = 138

        gravity_point = [0,0,0] # 重心点
        ax_roll_gp = 36 #回転軸と重心の距離
        body_to_gp = 58 # 重心とbodyの上端の距離

        self.left_arm_range = np.array([[-arm_width/2, ax_roll_gp,0],                 # min
                        [-arm_width/2, ax_roll_gp+self.arm_ground_size,0]])   # max
        
        self.right_arm_range = np.array([[arm_width/2, ax_roll_gp,0],                 # min
                        [arm_width/2, ax_roll_gp+self.arm_ground_size,0]])    # max

        self.min_deg = [ax_roll_gp/(-arm_width/2),     #有効範囲の最小の傾き
                   ax_roll_gp/(arm_width/2)]

        self.body_range = np.array([gravity_point,
                     [-body_width/2, self.min_deg[1]*(-body_width/2), 0],
                     [-body_width/2, -(body_length -body_to_gp -(body_length-body_ground_size[1]) /2), 0],
                     [body_width/2, -(body_length -body_to_gp -(body_length-body_ground_size[1]) /2), 0],
                     [body_width/2, self.min_deg[0] *(body_width /2),0],
                     ])

    # @classmethod
    def get_ground_range(self, debug=False):
        self.sim_calib = np.array([0, 36, 18 - self.plot_counter]) #[x,y(回転軸から重心の距離),z(モデルの高さ分)]
        self.plot_counter += 1 #描画の層を一層上にあげる
        body_range = self.body_range - self.sim_calib
        left_arm_range = self.left_arm_range -self.sim_calib
        right_arm_range = self.right_arm_range - self.sim_calib

        if debug :
            print("left_arm_range is :",left_arm_range)
            print("right_arm_range is :",right_arm_range)
            print("body_range is :",body_range)

        return left_arm_range.T,right_arm_range.T,body_range,[0,-36,0]
    
    def sort_list(self,debug=False):
        ps = []
        for i in range(len(self.body_range)):
            ps.append([self.body_range[i][0], self.body_range[i][1], self.body_range[i][2]])
        self.body_range=gift_wrap.wrap(ps)
        if debug:
            print("sort body range",self.body_range)
    
    def right_tilt_range(self,degree,debug=False): # 右側の傾きから有効範囲を計算
        print("左腕を曲げたとき右腕とボディの推定")
        tilt = math.tan(math.radians(degree)) #傾きの計算
        new_body_range = []

        if tilt*self.right_arm_range[0,0] > self.right_arm_range[1,1] : # 腕の接地点の範囲を超えたら
            # y=tilt *x +b
            b = self.right_arm_range[1,1]-tilt*self.right_arm_range[0,0] # 切片
            x = b/(self.min_deg[0]-tilt)  #交点 ax+b = Ax : b = Ax-ax : x = b/(A-a)
            y= self.min_deg[0]*x          #交点
            new_body_range.append([x,y,0]) #ボディーの範囲を更新
        else:
            b=0
            self.right_arm_range[1,1] = tilt*self.right_arm_range[0,0] # アームの有効範囲の更新
            new_body_range.append([0,0,0])
        
        #        x=(y-b)/a 
        if abs((self.body_range[2,1] - b) / tilt) < abs(self.body_range[2,0]) : # xが限界を超えていなければ
            #print("y max",self.body_range[2,1])
            new_body_range.append([(self.body_range[2,0]-b)/tilt, self.body_range[2,1], 0])
        elif abs(self.body_range[1,0]*tilt + b) < abs(self.body_range[2,1]): # yが限界を超えていなければ
            #print("x max",self.body_range[1,0]*tilt, abs(self.body_range[2,1]))
            new_body_range.append([self.body_range[1,0],self.body_range[1,0]*tilt+b,0])

        b = self.right_arm_range[0,1]-tilt*self.right_arm_range[0,0] #切片
        x = b/(self.min_deg[0]-tilt) #交点
        y= self.min_deg[0]*x         #交点

                #x = (y-b)/a
        if abs((self.body_range[2,1] - b) / tilt) < abs(self.body_range[2,0]) : # xが限界を超えていなければ
            new_body_range.append([(self.body_range[2,0]-b)/tilt,self.body_range[2,1],0])
        elif abs(self.body_range[1,0]*tilt + b) < abs(self.body_range[2,1]): # yがげんかいをかえてなければ
            new_body_range.append([self.body_range[1,0],self.body_range[1,0]*tilt+b,0])

        new_body_range.append([x,y,0])
        self.body_range = new_body_range

        if debug:
            print("tilt is ",tilt)
            print("b is",b)
            print("x is",(self.body_range[2,1] - b) / tilt)
            print("init body range is",self.body_range)
            print("new body range is",new_body_range)


    def left_arm_estimate(self,servo_deg,pitch_deg,debug=False):
        print("左腕を曲げたときの左腕とボディの推定")
        new_body_range = []
        self.body_range = np.array(self.body_range) #numpy化
        # l_body_max = self.left_arm_range[0,1] - min(self.body_range[:,1:2].T[0])
        # l_body_min = self.left_arm_range[0,1] - max(self.body_range[:,1:2].T[0])
        l_body_max = self.sim_calib[1] - min(self.body_range[:,1:2].T[0]) #回転軸からボディーの有効範囲の最大
        l_body_min = self.sim_calib[1] - max(self.body_range[:,1:2].T[0]) #回転軸からボディーの有効範囲の最小
        
        arm_deg = servo_deg - pitch_deg
        l_arm_max = l_body_max*math.sin(math.radians(pitch_deg))/math.sin(math.radians(arm_deg)) #回転軸からのアーム最大距離
        l_arm_min = l_body_min*math.sin(math.radians(pitch_deg))/math.sin(math.radians(arm_deg)) #回転軸からのアーム最小距離
        if debug :
            print("l body max/min is",l_body_max,l_body_min)
            print("slice data is ",self.body_range[:,1:2].T[0])
            print("arm_deg is ",arm_deg)
            print("arm max/min is:",l_arm_max,l_arm_min)
            print(len(self.body_range))        

        if l_arm_max > self.left_arm_range[1,1]-self.sim_calib[1] : # アームの限界値を超えたとき
            l_arm_max = self.left_arm_range[1,1]-self.sim_calib[1] # アームの最大値を代入
            l_body_max = l_arm_max*math.sin(math.radians(arm_deg))/math.sin(math.radians(pitch_deg)) #逆算してbodyの範囲を小さくする

            for i in range(len(self.body_range)-1) :
                if i == 0:
                    new_body_range.append(self.body_range[i])
                if abs(self.body_range[i+1,1]) > abs(l_body_max-self.sim_calib[1]): # y軸の推定範囲を超えたら
                    x_range=[self.body_range[i,0],self.body_range[i+1,0]]
                    a = (self.body_range[i+1,1]-self.body_range[i,1])/(self.body_range[i+1,0]-self.body_range[i,0])
                    b = self.body_range[i,1]-a*self.body_range[i,0]
                    if max(x_range)>= (self.left_arm_range[0,1]-l_body_max-b) / a >= min(x_range):
                        new_body_range.append([(self.left_arm_range[0,1]-l_body_max-b) / a, self.left_arm_range[0,1]-l_body_max, 0])
                        # self.body_range[i+1,0] = (self.left_arm_range[0,1]-l_body_max-b) / a   # x
                        # self.body_range[i+1,1] = self.left_arm_range[0,1]-l_body_max         # y

                    x_range=[self.body_range[i+1,0],self.body_range[i+2,0]]
                    a = (self.body_range[i+2,1]-self.body_range[i+1,1])/(self.body_range[i+2,0]-self.body_range[i+1,0])
                    b = self.body_range[i+1,1]-a*self.body_range[i+1,0]
                    if max(x_range)>=(self.left_arm_range[0,1]-l_body_max-b) / a >= min(x_range):
                        new_body_range.append([(self.left_arm_range[0,1]-l_body_max-b) / a, self.left_arm_range[0,1]-l_body_max, 0])
                        # self.body_range[i+1,0] = (self.left_arm_range[0,1]-l_body_max-b) / a   # x
                        # self.body_range[i+1,1] = self.left_arm_range[0,1]-l_body_max         # y
                else:
                    new_body_range.append(self.body_range[i+1])
            self.body_range=new_body_range
        else :
            # self.left_arm_range[0,1] = l_arm_min + self.sim_calib[1] 
            self.left_arm_range[1,1] = l_arm_max + self.sim_calib[1]

        if  l_arm_min >= self.left_arm_range[0,1]-self.sim_calib[1] : # アームの最小値を超えた場合 
            self.left_arm_range[0,1] = l_arm_min + self.sim_calib[1]
        
        else:
            l_arm_min = self.left_arm_range[0,1]-self.sim_calib[1] # アームの最大値を代入
            l_body_min = l_arm_min*math.sin(math.radians(arm_deg))/math.sin(math.radians(pitch_deg)) #逆算してbodyの範囲を小さくする

            for i in range(len(self.body_range)-1) :
                if i == 0:
                    new_body_range.append(self.body_range[i])
                if abs(self.body_range[i+1,1]) > abs(l_body_min-self.sim_calib[1]): # y軸の推定範囲を超えたら
                    x_range=[self.body_range[i,0],self.body_range[i+1,0]]
                    a = (self.body_range[i+1,1]-self.body_range[i,1])/(self.body_range[i+1,0]-self.body_range[i,0])
                    b = self.body_range[i,1]-a*self.body_range[i,0]
                    print("a=",a)
                    if max(x_range)>= (self.left_arm_range[0,1]-l_body_min-b) / a >= min(x_range):
                        new_body_range.append([(self.left_arm_range[0,1]-l_body_min-b) / a, self.left_arm_range[0,1]-l_body_min, 0])

                    x_range=[self.body_range[i+1,0],self.body_range[i+2,0]]
                    a = (self.body_range[i+2,1]-self.body_range[i+1,1])/(self.body_range[i+2,0]-self.body_range[i+1,0])
                    b = self.body_range[i+1,1]-a*self.body_range[i+1,0]
                    print("a=",a)
                    if max(x_range)>=(self.left_arm_range[0,1]-l_body_min-b) / a >= min(x_range):
                        new_body_range.append([(self.left_arm_range[0,1]-l_body_min-b) / a, self.left_arm_range[0,1]-l_body_min, 0])
                        # self.body_range[i+1,0] = (self.left_arm_range[0,1]-l_body_max-b) / a   # x
                        # self.body_range[i+1,1] = self.left_arm_range[0,1]-l_body_max         # y
                else:
                    new_body_range.append(self.body_range[i+1])

            self.body_range=new_body_range

            if debug : print("left_arm_range is :",self.left_arm_range)
    
    def left_tilt_range(self,degree,debug = False):
        print("右腕を曲げたときの左腕とボディの推定")
        tilt = math.tan(math.radians(degree))
        self.body_range = np.array(self.body_range) #numpy化
        new_body_range = []
             
        if tilt*self.left_arm_range[0,0] > self.left_arm_range[1,1] : # 腕の接地点の範囲を超えたら y
            # print("left arm ovar range")
            a = (self.body_range[0,1]-self.body_range[1,1])/(self.body_range[0,0]-self.body_range[1,0])
            # b = self.left_arm_range[1,1]-tilt*self.left_arm_range[0,0]
            b = self.body_range[0,1]-a*self.body_range[0,0]
            b2 = self.left_arm_range[1,1] - tilt*self.left_arm_range[1,0]
            x = (b2-b)/(a-tilt)             
            y= a*x +b
            new_body_range.append([x,y,0])
        else:
            b=0
            self.left_arm_range[1,1] = tilt*self.left_arm_range[0,0] # アームの有効範囲の更新
            new_body_range.append([0,0,0])
        
        for i in range(len(self.body_range)-1) :
            a = (self.body_range[i+1,1]-self.body_range[i,1])/(self.body_range[i+1,0]-self.body_range[i,0])
            b = self.body_range[i,1]-a*self.body_range[i,0]

            a2 = tilt
            b2 = self.left_arm_range[0,1]- a2*self.left_arm_range[0,0] #  arm min の交点
            b3 =self.left_arm_range[1,1] - a2*self.left_arm_range[1,0] # arm maxの交点

            if debug:
                print("y=",a,"x +",b)
                print("a2,b3,b3",a2,b2,b3)
                print("range is",min([self.body_range[i,0],self.body_range[i+1,0]]),max([self.body_range[i,0],self.body_range[i+1,0]]), (b-b2)/(a2-a))
                print("range is",min([self.body_range[i,0],self.body_range[i+1,0]]),max([self.body_range[i,0],self.body_range[i+1,0]]), (b-b3)/(a2-a))
            
            #交点がこの範囲で交わるなら
            if a2-a != 0 :
                if min([self.body_range[i,0],self.body_range[i+1,0]]) <= ((b-b2)/(a2-a)) <= max([self.body_range[i,0],self.body_range[i+1,0]]):
                        # print("in range",i,i+1)
                        # print("##########",[(b-b2)/(a2-a),(b-b2)/(a2-a)*a2+b2,0])
                        new_body_range.append([(b-b2)/(a2-a),(b-b2)/(a2-a)*a2+b2,0])
                
                if min([self.body_range[i,0],self.body_range[i+1,0]]) <= ((b-b3)/(a2-a)) <= max([self.body_range[i,0],self.body_range[i+1,0]]) and i!=0:
                        # print("in range of arm max",i,i+1)
                        # print("###########", [(b-b3)/(a2-a),(b-b3)/(a2-a)*a2+b3,0])
                        new_body_range.append([(b-b3)/(a2-a),(b-b3)/(a2-a)*a2+b3,0])
                
                if min([((b-b2)/(a2-a)),((b-b3)/(a2-a))]) <= self.body_range[i+1,0] <= max([((b-b2)/(a2-a)),((b-b3)/(a2-a))]):
                    new_body_range.append(self.body_range[i+1])
        
        if debug:
            print("tilt is ",tilt)
            print("pre body range is",self.body_range)
            print("new body range is",new_body_range)

        self.body_range = new_body_range


    def right_arm_estimate(self,servo_deg,pitch_deg,debug=False):
        print("右腕を曲げたときの右腕とボディの推定")
        new_body_range = []
        self.body_range = np.array(self.body_range)
        l_body_max = self.sim_calib[1] - min(self.body_range[:,1:2].T[0])
        l_body_min = self.sim_calib[1] - max(self.body_range[:,1:2].T[0])
        
        arm_deg = servo_deg - pitch_deg
        l_arm_max = l_body_max*math.sin(math.radians(pitch_deg))/math.sin(math.radians(arm_deg))
        l_arm_min = l_body_min*math.sin(math.radians(pitch_deg))/math.sin(math.radians(arm_deg)) 
        
        if debug:
            print("l body max is",l_body_max,l_body_min)
            print("slice data is ",self.body_range[:,1:2].T[0])
            print("arm max is:",l_arm_max,l_arm_min)
            print(len(self.body_range))        

        if l_arm_max > self.right_arm_range[1,1]-self.sim_calib[1] : # アームの限界値を変えたとき
            l_arm_max = self.right_arm_range[1,1]-self.sim_calib[1]# アームの最大値を代入
            l_body_max = l_arm_max*math.sin(math.radians(arm_deg))/math.sin(math.radians(pitch_deg)) #逆算してbodyの範囲を小さくする

            for i in range(len(self.body_range)-1) :
                if i == 0:
                    new_body_range.append(self.body_range[i])

                if abs(self.body_range[i+1,1]) > abs(l_body_max - self.sim_calib[1]): # y軸の推定範囲を超えたら
                    x_range=[self.body_range[i,0],self.body_range[i+1,0]]
                    a = (self.body_range[i+1,1]-self.body_range[i,1])/(self.body_range[i+1,0]-self.body_range[i,0])
                    b = self.body_range[i,1]-a*self.body_range[i,0]
                    if max(x_range)>= (self.right_arm_range[0,1]-l_body_max-b) / a >= min(x_range):
                        new_body_range.append([(self.right_arm_range[0,1]-l_body_max-b) / a, self.right_arm_range[0,1]-l_body_max, 0])
                        # self.body_range[i+1,0] = (self.right_arm_range[0,1]-l_body_max-b) / a   # x
                        # self.body_range[i+1,1] = self.right_arm_range[0,1]-l_body_max         # y
                    x_range=[self.body_range[i+1,0],self.body_range[i+2,0]]
                    a = (self.body_range[i+2,1]-self.body_range[i+1,1])/(self.body_range[i+2,0]-self.body_range[i+1,0])
                    b = self.body_range[i+1,1]-a*self.body_range[i+1,0]
                    if max(x_range)>= (self.right_arm_range[0,1]-l_body_max-b) / a >= min(x_range):
                        new_body_range.append([(self.right_arm_range[0,1]-l_body_max-b) / a, self.right_arm_range[0,1]-l_body_max, 0])

                else:
                    new_body_range.append(self.body_range[i+1])
            self.body_range=new_body_range
            new_body_range=[]  
        else :
            self.right_arm_range[1,1] = self.sim_calib[1] + l_arm_max
        
        if l_arm_min >= self.right_arm_range[0,1]-self.sim_calib[1] : # アームの限界値を変えたとき
            self.right_arm_range[0,1] = self.sim_calib[1] + l_arm_min
        else :
            pass
        if debug : print("arm range is",self.right_arm_range)
        
    def right_tilt_range2(self,degree,debug=False):
        print()
        print("2回目の左腕を曲げたときの右腕とボディの推定")
        tilt = math.tan(math.radians(degree))
        self.body_range = np.array(self.body_range) #numpy化
        new_body_range = []
        body_range_len =(len(self.body_range))# ボディ推定配列の長さ
             
        if tilt*self.right_arm_range[0,0]+max(self.body_range[:,1:2].T[0])> self.right_arm_range[1,1] : # 腕の接地点の範囲を超えたら y
            # print("left arm ovar range")
            a = (self.body_range[0,1]-self.body_range[body_range_len-1,1])/(self.body_range[0,0]-self.body_range[body_range_len-1,0])
            # b = self.left_arm_range[1,1]-tilt*self.left_arm_range[0,0]
            b = self.body_range[0,1]-a*self.body_range[0,0]
            b2 = self.right_arm_range[1,1] - tilt*self.right_arm_range[1,0]
            x = (b2-b)/(a-tilt)             
            y= a*x +b
            new_body_range.append([x,y,0])
        else:
            pass

        for i in range(len(self.body_range)) :
            if i < len(self.body_range)-1:
                a = (self.body_range[i+1,1]-self.body_range[i,1])/(self.body_range[i+1,0]-self.body_range[i,0])
                b = self.body_range[i,1]-a*self.body_range[i,0]
                x_range = [min([self.body_range[i,0],self.body_range[i+1,0]]),max([self.body_range[i,0],self.body_range[i+1,0]])] 
            else:
                a = (self.body_range[0,1]-self.body_range[i,1])/(self.body_range[0,0]-self.body_range[i,0])
                b = self.body_range[i,1]-a*self.body_range[i,0]
                x_range = [min([self.body_range[i,0],self.body_range[0,0]]),max([self.body_range[i,0],self.body_range[0,0]])] 

            a2 = tilt
            b2 = self.right_arm_range[0,1]- a2*self.right_arm_range[0,0] #  arm min の交点
            b3 =self.right_arm_range[1,1] - a2*self.right_arm_range[1,0] # arm maxの交点

            if debug:
                print("i=",i)
                print("body range len",len(self.body_range-1))
                print("y=",a,"x +",b)
                print("range is", x_range, (b-b2)/(a2-a),(b-b3)/(a2-a))
            
            #交点がこの範囲で交わるなら
            if min([((b-b2)/(a2-a)),((b-b3)/(a2-a))]) <= self.body_range[i,0] <= max([((b-b2)/(a2-a)),((b-b3)/(a2-a))]):
                new_body_range.append(self.body_range[i])

            if x_range[0] <= ((b-b2)/(a2-a)) <= x_range[1]:
                    # print("in range",i,i+1)
                    # print("##########",[(b-b2)/(a2-a),(b-b2)/(a2-a)*a2+b2,0])
                    new_body_range.append([(b-b2)/(a2-a),(b-b2)/(a2-a)*a2+b2,0])
            
            if x_range[0] <= ((b-b3)/(a2-a)) <= x_range[1]:
                    # print("in range of arm max",i,i+1)
                    # print("###########", [(b-b3)/(a2-a),(b-b3)/(a2-a)*a2+b3,0])
                    new_body_range.append([(b-b3)/(a2-a),(b-b3)/(a2-a)*a2+b3,0])
            
            
        
        if debug:
            print("tilt is ",tilt)
            print("init body range is",self.body_range)
            print("new body range is",new_body_range)

        self.body_range = new_body_range
