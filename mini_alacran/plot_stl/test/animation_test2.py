import collections
import math
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from mpl_toolkits.mplot3d import Axes3D
from stl import mesh

import sys
sys.path.append('./../script/')
from rotation_matrix import RotationMatrix
from mesh_adj import MeshAdj

class SimulationWorld():
    def __init__(self, time_span, time_interval):
        self.objects = []
        self.time_span = time_span
        self.time_interval = time_interval

    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d', proj_type='persp')
        self.scale = self.robots.final_robot.points.flatten()
        ax.auto_scale_xyz(self.scale, self.scale, self.scale) 
        collection = Poly3DCollection(self.robots.final_robot.vectors,color='w',alpha=0.2,edgecolor='k') 
        # collection = Line3DCollection(self.robots.final_robot.vectors, colors='k', linewidths=0.2, linestyles=':')
        ax.add_collection3d(collection)
        anim = animation.FuncAnimation(fig, self.one_step, fargs=(collection,ax),
                                    frames=360, interval=1000 / 30,blit=True)
        plt.show()

    
    def append(self,obj): #Robotが追加された時の処理
        self.objects.append(obj)
        if isinstance(obj, Robot): self.robots = obj

    def one_step(self,frame,collection,ax):
        for obj in self.objects:
            # if hasattr(obj, "draw"):
            #     obj.draw(ax, collection)
            if hasattr(obj, "one_step"):
                obj.one_step(frame,ax,collection,self.scale)
        ax.auto_scale_xyz([-150,150], [-150,150], [-150,150]) 
        return collection,ax

class Robot():
    def __init__(self, first_robot) :
        self.robot_mesh={}
        self.parts_name_list = []

        for parts_data in first_robot:
            parts_name = parts_data[0]
            print(parts_name)
            mesh_data = parts_data[1]
            init_param = parts_data[2]
            mesh_data =MeshAdj.mesh_location_zero(mesh_data,init_param)
            self.parts_add(parts_name,mesh_data)
            self.init_rotation(parts_name, 90)


    def parts_add(self,parts_name,mesh_data):
        self.parts_name_list.append(parts_name)
        self.robot_mesh[parts_name] = [mesh_data, 0]
        self.robot_update()

    def init_rotation(self, parts_name, deg):
        R = np.zeros((4, 4))
        R[3,3] = 1
        R[:3, :3] = tuple(RotationMatrix.x(deg)) #回転行列
        R[:3,3:] = [[0],[0],[0]]
        self.robot_mesh[parts_name][0].transform(R)
        self.robot_update()

    def parts_rotation(self, parts_name, deg):
        now_deg = self.robot_mesh[parts_name][1]
        move_deg = deg - now_deg
        R = np.zeros((4, 4))
        R[3,3] = 1
        R[:3, :3] = tuple(RotationMatrix.x(move_deg)) #回転行列
        R[:3,3:] = [[0],[0],[0]]
        self.robot_mesh[parts_name][0].transform(R)
        self.robot_mesh[parts_name][1] = deg
        self.robot_update()

    
    def robot_update(self):
        comb_robot=[]
        # meshデータの更新
        for i in range(len(self.parts_name_list)):
            self.robot_mesh[self.parts_name_list[i]][0] = MeshAdj.mesh_update(self.robot_mesh[self.parts_name_list[i]][0])
        # meshデータの結合
        for mesh_data in self.robot_mesh.values(): 
            comb_robot.append(mesh_data[0].data.copy())
        self.final_robot = mesh.Mesh(np.concatenate(comb_robot))
        return self.final_robot 
    
    def parts_center_point(self):
        points = []
        for mesh_data in self.robot_mesh.values():
            points.append(MeshAdj.get_mesh_center(mesh_data[0]))
        return points


    def one_step(self,frame, ax,collection,scale):
        self.parts_rotation("body",-20)
        # print("frame",-30)
        self.parts_rotation("left arm",20)
        self.parts_rotation("right arm",-20)
        points = np.array(self.parts_center_point())
        print("point=",points)
        ax.clear()
        collection.set_verts(self.final_robot.vectors)
        collection.do_3d_projection(collection.axes.get_figure().canvas.get_renderer())
        ax.scatter(points[:,0:1], points[:,1:2], points[:,2:3], s = 200, c = "red")
        # for ln in points: c = ax.scatter(points[0], points[1], points[2], s=100, marker="*", label="landmarks", color="orange")


def trial():

    world=SimulationWorld(30,0.1)
    
    # meshの読み込み
    body_mesh = mesh.Mesh.from_file('../../stl/low_model/body.stl')
    left_arm_mesh = mesh.Mesh.from_file('../../stl/low_model/flipper-arm.stl')
    right_arm_mesh = mesh.Mesh.from_file('../../stl/low_model/flipper-arm.stl')

    # 位置の調整
    body_init_pos = [0,0,-53.036]
    left_arm_init_pos = [83.4,0,44.25]
    right_arm_init_pos = [-83.4,0,44.25]

    body_data = ["body",body_mesh,body_init_pos]
    left_arm_data = ["left arm", left_arm_mesh,left_arm_init_pos]
    right_arm_data = ["right arm", right_arm_mesh, right_arm_init_pos]

    robot = Robot([body_data,left_arm_data,right_arm_data])
    world.append(robot)

    world.draw()



if __name__ == "__main__":
    trial()