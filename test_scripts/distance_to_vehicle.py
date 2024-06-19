from pypcd import pypcd
import numpy as np
import sys
import math

if __name__=="__main__":
    pc = pypcd.PointCloud.from_path(sys.argv[1])
    pc_data = pc.pc_data
    pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["label"]], dtype=np.float32)
    # reshape pc array 
    pc_array = np.transpose(pc_array)
    # save np array to file
    pc_header = np.array(pc.viewpoint, dtype=np.float32)
    print(pc_header)
    min_distance = float('inf')
    for row in pc_array:
        if row[3] == 6.0:
            distance = math.sqrt((row[0])**2 + 
                                 (row[1])**2 + 
                                 (row[2])**2)
            if distance < min_distance:
                min_distance = distance
                print(row)
    print(min_distance)
    #print(pc_array)
