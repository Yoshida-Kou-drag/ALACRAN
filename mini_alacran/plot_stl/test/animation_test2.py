import collections
import math
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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
        scale = self.robots.final_robot.points.flatten()
        ax.auto_scale_xyz(scale, scale, scale) 
        collection = Poly3DCollection(self.robots.final_robot.vectors,color='w',alpha=0.4,edgecolor='k') 
        ax.add_collection3d(collection)
        anim = animation.FuncAnimation(fig, self.one_step, fargs=(collection,ax),
                                    frames=360, interval=1000 / 30,blit=True)
        plt.show()

    
    def append(self,obj): #Robotが追加された時の処理
        self.objects.append(obj)
        if isinstance(obj, Robot): self.robots = obj

    def one_step(self,frame,collection,ax):
        for obj in self.objects:
            if hasattr(obj, "one_step"):
                obj.one_step(frame)
                collection.set_verts(obj.final_robot.vectors)
                collection.do_3d_projection(collection.axes.get_figure().canvas.get_renderer())
                # ax.add_collection3d(collection) 
        return collection,ax

class Robot():
    def __init__(self) :
        self.robot_mesh={}
        
    
    def parts_add(self,parts_name,mesh_data):
        self.robot_mesh[parts_name] = mesh_data
        self.robot_update()
    
    def parts_rotation(self, parts_name, deg):
        R = np.zeros((4, 4))
        R[3,3] = 1
        R[:3, :3] = tuple(RotationMatrix.x(deg)) #回転行列
        R[:3,3:] = [[0],[0],[0]]
        self.robot_mesh[parts_name].transform(R)
        self.robot_update()
    
    def robot_update(self):
        comb_robot=[]
        for mesh_data in self.robot_mesh.values(): 
            comb_robot.append(mesh_data.data.copy())
        self.final_robot = mesh.Mesh(np.concatenate(comb_robot))
        return self.final_robot 


    def one_step(self,frame):
        self.parts_rotation("body_mesh",1)



def trial():

    world=SimulationWorld(30,0.1)
    robot = Robot()
    world.append(robot)
    body_mesh = mesh.Mesh.from_file('../../stl/low_model/body.stl')
    body_init_pos = [0,0,-53.036]
    body_mesh = MeshAdj.mesh_location_zero(body_mesh,body_init_pos)
    robot.parts_add('body_mesh',body_mesh)
    world.draw()





if __name__ == "__main__":
    trial()