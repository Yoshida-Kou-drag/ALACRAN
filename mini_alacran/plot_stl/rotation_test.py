from operator import le
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from rotation_matrix import RotationMatrix

def mesh_scale(my_mesh, scale_x, scale_y, scale_z):
    my_mesh.x = my_mesh.x * scale_x
    my_mesh.y = my_mesh.y * scale_y
    my_mesh.z = my_mesh.z * scale_z 
    return my_mesh

def mesh_location_zero(my_mesh):
    midPosRel = (my_mesh.max_ - my_mesh.min_)/2
    my_mesh.x = my_mesh.x - (midPosRel[0] + my_mesh.min_[0])
    my_mesh.y = my_mesh.y - (midPosRel[1] + my_mesh.min_[1])
    my_mesh.z = my_mesh.z - (19.750 + my_mesh.min_[2])
    return my_mesh, midPosRel

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

left_arm_mesh = mesh.Mesh.from_file('../stl/low_model/flipper-arm.stl')
left_arm_mesh, midpos = mesh_location_zero(left_arm_mesh)
print("mid pos is :",midpos)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(left_arm_mesh.vectors))


R = np.zeros((4, 4))
R[3,3] = 1
R[:3, :3] = tuple(RotationMatrix.x(60)) 
# R[0:3,3:] = [[0],[-midpos[1]],[-midpos[2]]]
R[:3,3:] = [[0],[0],[0]]
print("rotation matrix is:",R[:3,3:])
left_arm_mesh.transform(R)

# my_mesh = mesh_scale(my_mesh,0.1, 0.1, 0.1) #大きさの調整
# cube_comb = mesh_location_zero(cube_comb)   #原点合わせ
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(left_arm_mesh.vectors))
scale = left_arm_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

pyplot.show()