from operator import le
from turtle import color
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

import sys
sys.path.append('./script/')
from rotation_matrix import RotationMatrix
from mesh_adj import MeshAdj


figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# meshの読み込み
body_mesh = mesh.Mesh.from_file('../stl/low_model/body.stl')
left_arm_mesh = mesh.Mesh.from_file('../stl/low_model/flipper-arm.stl')
right_arm_mesh = mesh.Mesh.from_file('../stl/low_model/flipper-arm.stl')

# 位置の調整
body_init_pos = [0,0,-53.036]
left_arm_init_pos = [83.4,0,44.25]
right_arm_init_pos = [-83.4,0,44.25]

body_mesh = MeshAdj.mesh_location_zero(body_mesh,body_init_pos)
left_arm_mesh = MeshAdj.mesh_location_zero(left_arm_mesh,left_arm_init_pos)
right_arm_mesh = MeshAdj.mesh_location_zero(right_arm_mesh,right_arm_init_pos)

R = np.zeros((4, 4))
R[3,3] = 1
R[:3, :3] = tuple(RotationMatrix.x(90)) #回転行列
R[:3,3:] = [[0],[0],[0]]                #並進ベクトル
print("rotation matrix is:",R)
body_mesh.transform(R)
left_arm_mesh.transform(R)
right_arm_mesh.transform(R)


# 最終出力
cube_comb = mesh.Mesh(np.concatenate([
    body_mesh.data.copy(),
    left_arm_mesh.data.copy(),
    right_arm_mesh.data.copy(),
]))
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube_comb.vectors))
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube_comb.vectors,color='w',alpha=0.4,edgecolor='k'))

print(cube_comb.max_[0] - cube_comb.min_[0])

scale = cube_comb.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

body_mesh = MeshAdj.mesh_update(body_mesh)
points = MeshAdj.get_mesh_center(body_mesh)
axes.scatter(points[0], points[1], points[2], s = 40, c = "blue")


pyplot.show()