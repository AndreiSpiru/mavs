import open3d as o3d
import numpy as np

if __name__=="__main__":
    cloud = o3d.io.read_point_cloud('test.pcd')
    output = np.asarray(cloud.points)
    rows, cols = output.shape
    zeros = np.zeros((rows, 1))
    output = np.append(output, zeros, axis = 1)
    np.save("test_no_intensity", output)