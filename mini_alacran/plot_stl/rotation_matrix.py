import numpy as np

class RotationMatrix():
    @classmethod
    def x(self, degree):
        matrix = np.array([[1, 0, 0],
                            [0,np.cos(np.deg2rad(degree)), - np.sin(np.deg2rad(degree))],
                            [0,np.sin(np.deg2rad(degree)), np.cos(np.deg2rad(degree))]])
        return matrix

    def y(self, degree):
        matrix = np.array([[np.cos(np.deg2rad(degree)), 0, np.sin(np.deg2rad(degree))],
                           [0, 1, 0],
                           [-np.sin(np.deg2rad(degree)), 0, np.cos(np.deg2rad(degree))]])
        return matrix

    def z(self, degree):
        matrix = np.array([[np.cos(np.deg2rad(degree)), - np.sin(np.deg2rad(degree)), 0],
                           [np.sin(np.deg2rad(degree)), np.cos(np.deg2rad(degree)), 0],
                           [0, 0, 1]])
        return matrix

