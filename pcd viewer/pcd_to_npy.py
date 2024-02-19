from pypcd import pypcd
import numpy as np

if __name__=="__main__":
    pc = pypcd.PointCloud.from_path("test.pcd")
    pc_data = pc.pc_data
    pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["intensity"]], dtype=np.float32)
    # reshape pc array 
    pc_array = np.transpose(pc_array)
    # save np array to file
    np.save("test.npy", pc_array)
    print(pc_array)