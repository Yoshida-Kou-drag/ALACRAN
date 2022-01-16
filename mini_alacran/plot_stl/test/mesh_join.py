from operator import le
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

body_mesh = mesh.Mesh.from_file('../../stl/low_model/body.stl')
left_arm_mesh = mesh.Mesh.from_file('../../stl/low_model/flipper-left.stl')
right_arm_mesh = mesh.Mesh.from_file('../../stl/low_model/flipper-right.stl')
R = np.zeros((4, 4))
R[3,3] = 1
R[:3, :3] = tuple(RotationMatrix.x(60)) 
R[:3,3:] = [[10],[0],[0]]
print("rotation matrix is:",R[:3,3:])
right_arm_mesh.transform(R)

cube_comb = mesh.Mesh(np.concatenate([
    body_mesh.data.copy(),
    left_arm_mesh.data.copy(),
    right_arm_mesh.data.copy(),
]))
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube_comb.vectors))

scale = cube_comb.points.flatten()
print("Robot state is:",cube_comb.x)
axes.auto_scale_xyz(scale, scale, scale)

pyplot.show()