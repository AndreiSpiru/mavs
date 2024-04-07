import pypcd
import numpy as np

def get_bounding_box(file):
    pc = pypcd.PointCloud.from_path(filepath)
    pc_data = pc.pc_data
    count = 0
    pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["label"]], dtype=np.float32)
    pc_array = np.transpose(pc_array)
    vehicle_points = pc_array[pc_array[:,3] == 6.0]
    print(vehicle_points)
    vehicle_points = vehicle_points[:, :-1]
    print(vehicle_points)
file = 'output_data_converted/0-10/velodyne/0_labeled.pcd'
get_bounding_box(file)