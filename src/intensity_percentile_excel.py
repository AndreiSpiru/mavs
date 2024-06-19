import os
import pandas as pd
import numpy as np
from pypcd import pypcd
import math

def roi_filter(points, roi_min=(0,-35,-35), roi_max=(35,35,35)):

    mask_roi = np.logical_and.reduce((
        points[:, 0] >= roi_min[0],
        points[:, 0] <= roi_max[0],
        abs(points[:, 1] / points[:, 0]) <= 5,
        points[:, 1] >= roi_min[1],
        points[:, 1] <= roi_max[1],
        points[:, 2] >= roi_min[2],
        points[:, 2] <= roi_max[2]
    ))

    roi_points = points[mask_roi]

    return roi_points
    
def process_files_and_create_excel(root_directory, output_excel):
    # Create an empty DataFrame to store all data
    df = pd.DataFrame(columns=['File Name', 'Sensor Type', 'Condition', 'Intensity Percentile 50', 'Intensity Percentile 90', 'Intensity Percentile 95', 'Intensity Percentile 99'	])

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
                                pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["label"], pc_data["intensity"]], dtype=np.float32)
                                # reshape pc array 
                                pc_array = np.transpose(pc_array)
                                pc_array = roi_filter(pc_array)
                          
                                mask = pc_array[:, 3] == 6.0
                                vehicle_points = pc_array[mask]
                                # Extract intensity values
                                intensities = [point[4] for point in vehicle_points]
                                intensities = np.array(intensities)

                                # Define desired percentiles
                                percentiles = [50, 90, 95, 99]
                                if len(intensities) > 0:
                                    # Calculate percentile values
                                    percentile_values = np.percentile(intensities, percentiles)
                                else:
                                    percentile_values = [np.nan] * len(percentiles)
                                df = df._append({'File Name': filename, 'Sensor Type': sensor_type, 'Condition': condition, 
                                                 'Intensity Percentile 50': percentile_values[0], 'Intensity Percentile 90': percentile_values[1]
                                                 ,'Intensity Percentile 95': percentile_values[2], 'Intensity Percentile 99': percentile_values[3]},
                                                   ignore_index=True)

    # Write DataFrame to Excel
    df.to_excel(output_excel, index=False)
    print(f"Excel file created at: {output_excel}")
# Example usage:
root_directory = 'output_data_new/0-10'
output_excel = 'intensity_percentiles.xlsx'
process_files_and_create_excel(root_directory, output_excel)
