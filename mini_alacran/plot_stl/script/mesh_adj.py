# 読み込んだメッシュの調整
# 一つ一つのSTLデータにインスタンス化して与える

import numpy as np
from stl import mesh

class MeshAdj() :
    @classmethod
    def mesh_scale(my_mesh, scale_x, scale_y, scale_z):
        my_mesh.x = my_mesh.x * scale_x
        my_mesh.y = my_mesh.y * scale_y
        my_mesh.z = my_mesh.z * scale_z 
        return my_mesh

    def mesh_location_zero(my_mesh,axis=[0,0,0]):
        midPosRel = (my_mesh.max_ - my_mesh.min_)/2
        my_mesh.x = my_mesh.x - (midPosRel[0] + my_mesh.min_[0])+axis[0]
        my_mesh.y = my_mesh.y - (midPosRel[1] + my_mesh.min_[1])+axis[1]
        my_mesh.z = my_mesh.z - (midPosRel[2] + my_mesh.min_[2])+axis[2]
        return my_mesh

    def get_mesh_center(my_mesh):
        midPosRel = (my_mesh.max_ - my_mesh.min_)/2 + my_mesh.min_
        return midPosRel

    def mesh_update(my_mesh):
        my_mesh.update_areas()
        my_mesh.update_max()
        my_mesh.update_min()
        my_mesh.update_units()
        return my_mesh
    