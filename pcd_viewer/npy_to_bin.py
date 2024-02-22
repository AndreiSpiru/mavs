import numpy as np
import sys

if __name__=="__main__":
    pc = np.load(sys.argv[1])
    pc.astype(np.float32).tofile(sys.argv[1][:-3] + "bin")