import open3d as o3d
import numpy as np

if __name__=="__main__":
    cloud = o3d.io.read_point_cloud('test.pcd')
    output = cloud.points
    rows, cols = output.shape
    append = np.zeroes(rows, cols + 1)
    output[:,:-1] = append
    np.save("test_no_intensity", cloud.points)