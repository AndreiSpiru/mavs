from pypcd import pypcd
import numpy as np
import sys

if __name__=="__main__":
    pc = pypcd.PointCloud.from_path(sys.argv[1])
    pc_data = pc.pc_data
    pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["intensity"]], dtype=np.float32)
    # reshape pc array 
    pc_array = np.transpose(pc_array)
    # save np array to file
    np.save(sys.argv[1][:-3] + "npy", pc_array)
    print(pc_array)