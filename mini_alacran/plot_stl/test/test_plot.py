import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from cube_model import cube_model

figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

your_mesh = cube_model(10,10,10)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

scale = your_mesh.points.flatten()
print(scale)
axes.auto_scale_xyz(scale, scale, scale)

pyplot.show()