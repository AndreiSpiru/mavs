import os
import pandas as pd
import numpy as np
from pypcd import pypcd
import math

def process_files_and_create_excel(root_directory, output_excel):
    # Create an empty DataFrame to store all data
    df = pd.DataFrame(columns=['File Name', 'Sensor Type', 'Condition'])

    # Iterate through subdirectories and process files
    for sensor_type in os.listdir(root_directory):
        sensor_path = os.path.join(root_directory, sensor_type)
        if os.path.isdir(sensor_path):
            for condition in os.listdir(sensor_path):
                condition_path = os.path.join(sensor_path, condition)
                if os.path.isdir(condition_path):
                    # Process files in the current condition directory
                    for root, dirs, files in os.walk(condition_path):
                        for filename in files:
                            
                            # # Read data from file (replace this with your own logic)
                            # with open(filepath, 'r') as file:
                            #     data = file.read().strip()  # Read and strip whitespace
                            
                            # # Add data to DataFrame
                            if filename.endswith('.pcd'):
                                filepath = os.path.join(root, filename)
                                print(filepath)
                                pc = pypcd.PointCloud.from_path(filepath)
                                pc_data = pc.pc_data
                                count = 0
                                pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["label"]], dtype=np.float32)
                                # reshape pc array 
                                pc_array = np.transpose(pc_array)
                                # save np array to file
                                min_distance = float('inf')
                                for row in pc_array:
                                    if row[3] == 6.0:
                                        count += 1
                                        distance = math.sqrt((row[0] )**2 + 
                                                            (row[1])**2 + 
                                                            (row[2])**2)
                                        if distance < min_distance:
                                            min_distance = distance
                                df = df._append({'File Name': filename, 'Sensor Type': sensor_type, 'Condition': condition, 'Vehicle Detected Points': count, 'Distance to vehicle': min_distance}, ignore_index=True)

    # Write DataFrame to Excel
    df.to_excel(output_excel, index=False)
    print(f"Excel file created at: {output_excel}")
# Example usage:
root_directory = 'output_data_converted/0-10'
output_excel = 'output_data.xlsx'
process_files_and_create_excel(root_directory, output_excel)