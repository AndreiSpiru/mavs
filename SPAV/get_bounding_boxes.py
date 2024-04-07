from cmath import inf
from pypcd import pypcd
import open3d as o3d
import numpy as np

def roi_filter(points, roi_min=(0,-inf,-inf), roi_max=(inf,inf,inf)):

    mask_roi = np.logical_and.reduce((
        points[:, 0] >= roi_min[0],
        points[:, 0] <= roi_max[0],
        points[:, 1] >= roi_min[1],
        points[:, 1] <= roi_max[1],
        points[:, 2] >= roi_min[2],
        points[:, 2] <= roi_max[2]
    ))

    roi_points = points[mask_roi]

    # Create a new point cloud with the filtered points
    roi_pcd = o3d.geometry.PointCloud()
    roi_pcd.points = o3d.utility.Vector3dVector(roi_points)
    return roi_pcd

def get_bounding_box(file):
    pc = pypcd.PointCloud.from_path(file)
    pc_data = pc.pc_data
    count = 0
    pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["label"]], dtype=np.float32)
    pc_array = np.transpose(pc_array)
    vehicle_points = pc_array[pc_array[:,3] == 6.0]
    vehicle_points = vehicle_points[:, :-1]
    pcd = roi_filter(vehicle_points)
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(vehicle_points)
    aabb = pcd.get_axis_aligned_bounding_box()
    aabb.color = (1, 0, 0)
    obb = pcd.get_oriented_bounding_box()
    obb.color = (0, 1, 0)
    centers = aabb.get_center()
    extent = aabb.get_extent()
    print(centers)
    print(extent)
    converted_bbox = np.concatenate((centers, extent), axis = 0)
    converted_bbox = np.append(converted_bbox, 0.0)
    print(converted_bbox)
    o3d.visualization.draw_geometries([pcd, aabb, obb])
file = 'output_data_converted/0-10/HDL-64E/clear/21_labeled.pcd'
get_bounding_box(file)