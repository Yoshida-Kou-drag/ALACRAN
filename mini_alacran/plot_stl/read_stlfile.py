import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

def mesh_scale(my_mesh, scale_x, scale_y, scale_z):
    my_mesh.x = my_mesh.x * scale_x
    my_mesh.y = my_mesh.y * scale_y
    my_mesh.z = my_mesh.z * scale_z 
    return my_mesh

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

my_mesh = mesh.Mesh.from_file('../stl/flipper-left.stl')
# my_mesh = mesh_scale(my_mesh,0.1, 0.1, 0.1)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(my_mesh.vectors))

scale = my_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

pyplot.show()