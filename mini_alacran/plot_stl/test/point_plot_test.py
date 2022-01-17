import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib

print(matplotlib.__version__)
# 3.0.3
#for 3D plotting
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    N = 100
    X = np.random.rand(N, 3)*100
    y = np.random.rand(N) * 2 - 1

    fig = plt.figure()

    ax2 = fig.add_subplot(111, projection='3d')
    sc2=ax2.scatter3D(np.ravel(X[:, 0]), np.ravel(X[:, 1]), zs=X[:, 2],zdir='z',s=50, vmin=0, vmax=1, c=y, cmap=plt.cm.jet)
    plt.colorbar(sc2)
    plt.show()