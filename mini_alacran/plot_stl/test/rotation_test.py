from operator import le
from turtle import color
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

import sys
sys.path.append('../script/')
from rotation_matrix import RotationMatrix
from mesh_adj import MeshAdj

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)
left_arm_init_pos = [0,0,44.25]

left_arm_mesh = mesh.Mesh.from_file('../../stl/low_model/flipper-arm.stl')

left_arm_mesh = MeshAdj.mesh_location_zero(left_arm_mesh,left_arm_init_pos)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(left_arm_mesh.vectors))


R = np.zeros((4, 4))
R[3,3] = 1
R[:3, :3] = tuple(RotationMatrix.x(60)) #回転行列
R[:3,3:] = [[0],[0],[0]]                #並進ベクトル
print("rotation matrix is:",R)
left_arm_mesh.transform(R)

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(left_arm_mesh.vectors))
scale = left_arm_mesh.points.flatten()

MeshAdj.mesh_update(left_arm_mesh)

R[:3, :3] = tuple(RotationMatrix.x(90)) #回転行列
R[:3,3:] = [[0],[0],[0]]                #並進ベクトル
print("rotation matrix is:",R)
left_arm_mesh.transform(R)

axes.add_collection3d(mplot3d.art3d.Poly3DCollection(left_arm_mesh.vectors,color='g'))
axes.auto_scale_xyz(scale, scale, scale)

pyplot.show()