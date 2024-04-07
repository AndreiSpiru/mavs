from pypcd import pypcd
import numpy as np
import sys
import os

def save_npy(directory, filename):
    filepath = os.path.join(directory, filename)
    pc = pypcd.PointCloud.from_path(filepath)
    pc_data = pc.pc_data
    pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["intensity"]], dtype=np.float32)
    # reshape pc array 
    pc_array = np.transpose(pc_array)
    # save np array to file
    filename = filename[:-3] + "npy"
    filepath = os.path.join(directory, filename)
    np.save(filepath, pc_array)

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
            save_npy(directory, filename)
if __name__=="__main__":
    process_files_in_subdirectories('output_data_converted', '.pcd')