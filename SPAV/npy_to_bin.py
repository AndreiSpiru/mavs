from pypcd import pypcd
import numpy as np
import sys
import os

def npy_to_bin(directory, filename):
    filepath = os.path.join(directory, filename)
    pc = np.load(filepath)
    filename = filename[:-3] + "bin"
    filepath = os.path.join(directory, filename)
    pc.astype(np.float32).tofile(filepath)

def process_files_in_subdirectories(root_directory, extension):
    # Walk through all subdirectories recursively
    for root, dirs, files in os.walk(root_directory):
        # Process files in the current directory
        process_files_in_directory(root, extension)

def process_files_in_directory(directory, extension):
    print(directory)
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        print(filepath)
        # Check if it's a file and has the desired extension
        if os.path.isfile(filepath) and filename.endswith(extension):
            npy_to_bin(directory, filename)
if __name__=="__main__":
    process_files_in_subdirectories('output_data_converted', '.npy')