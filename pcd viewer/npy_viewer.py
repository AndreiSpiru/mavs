import numpy as np
import sys

if __name__=="__main__":
    pc_array = np.load(sys.argv[1])
    print(pc_array)
    print(pc_array.shape)