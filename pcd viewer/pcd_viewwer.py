import open3d as o3d
import numpy as np

if __name__=="__main__":
    cloud = o3d.io.read_point_cloud('test.pcd')
    print(np.asarray(cloud.points))
    print(np.asarray(cloud.colors))
    print(np.asarray(cloud.normals))
    o3d.visualization.draw_geometries([cloud])