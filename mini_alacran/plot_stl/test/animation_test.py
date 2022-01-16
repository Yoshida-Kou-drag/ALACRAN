import math
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def visualize_rotation(frame, collection):
    angle = math.radians(2) * frame

    points = np.array([[-1, -1, -1],
                       [1, -1, -1],
                       [1, 1, -1],
                       [-1, 1, -1],
                       [-1, -1, 1],
                       [1, -1, 1],
                       [1, 1, 1],
                       [-1, 1, 1]])

    Z = np.zeros((8, 3))
    for i in range(8):
        Z[i, :] = [
            math.cos(angle) * points[i, 0] - math.sin(angle) * points[i, 1],
            math.sin(angle) * points[i, 0] + math.cos(angle) * points[i, 1],
            points[i, 2]
        ]
    Z = 10.0 * Z

    # list of sides' polygons of figure
    vertices = [[Z[0], Z[1], Z[2], Z[3]],
                [Z[4], Z[5], Z[6], Z[7]],
                [Z[0], Z[1], Z[5], Z[4]],
                [Z[2], Z[3], Z[7], Z[6]],
                [Z[1], Z[2], Z[6], Z[5]],
                [Z[4], Z[7], Z[3], Z[0]]]

    # plot sides
    collection.set_verts(vertices)
    collection.do_3d_projection(collection.axes.get_figure().canvas.get_renderer())
    print(frame)

    return [collection]

def init_func(ax, collection):
    # ax.clear()
    # ax.add_collection3d(collection)
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-15, 15)

    ax.set_box_aspect(np.ptp([ax.get_xlim(), ax.get_ylim(), ax.get_zlim()], axis=1))

    return [collection]

def animate_rotation():

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', proj_type='persp')

    collection = Poly3DCollection([[np.zeros(3)]], facecolors='white',
                                  linewidths=1, edgecolors='r', alpha=0.8)
    ax.add_collection3d(collection)

    # noinspection PyUnusedLocal
    anim = animation.FuncAnimation(fig, visualize_rotation, fargs=[collection],
                                   init_func=partial(init_func, ax, collection),
                                   frames=360, interval=1000 / 30, blit=True)

    plt.show()

animate_rotation()