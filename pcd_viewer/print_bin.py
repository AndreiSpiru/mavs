import numpy as np
import sys

if __name__=="__main__":
    with open(sys.argv[1], "rb") as file:
        binary_data = file.read()

    # Print the contents of the file
    print(binary_data)