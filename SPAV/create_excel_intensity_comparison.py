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
                                pc_array = np.array([pc_data["x"], pc_data["y"], pc_data["z"], pc_data["label"], pc_data["intensity"]], dtype=np.float32)
                                # reshape pc array 
                                pc_array = np.transpose(pc_array)
                                pc_array = roi_filter(pc_array)
                                # Calculate the Euclidean distance of each point from the origin (0, 0, 0)
                                distances = np.linalg.norm(pc_array[:, :3], axis=1)

                                # Find the maximum distance
                                max_distance = np.max(distances)
                                average_distance = np.mean(distances)
                                # save np array to file
                                min_distance = float('inf')
                                intensity_sum = 0
                                if condition == 'clear':
                                    rain_rate = 0
                                elif condition == 'light':
                                    rain_rate = 2.5
                                elif condition == 'moderate':
                                    rain_rate = 5
                                elif condition == 'heavy':
                                    rain_rate = 10.0    
                                elif condition == 'extreme':
                                    rain_rate = 25.0
                                for row in pc_array:
                                    if row[3] == 6.0:
                                        count += 1
                                        intensity_sum += row[4]
                                        distance = math.sqrt((row[0] )**2 + 
                                                            (row[1])**2 + 
                                                            (row[2])**2)
                                        if distance < min_distance:
                                            min_distance = distance
                                average_intensity = 0
                                if count > 0:
                                    average_intensity = intensity_sum / count
                                
                                predicted_intensity = average_intensity
                                if rain_rate >0:
                                    filepath_clear = filepath.replace(condition, 'clear')
                                    pc1 = pypcd.PointCloud.from_path(filepath_clear)
                                    pc_data1 = pc1.pc_data
                                    pc_array1 = np.array([pc_data1["x"], pc_data1["y"], pc_data1["z"], pc_data1["label"], pc_data1["intensity"]], dtype=np.float32)
                                    # reshape pc array 
                                    pc_array1 = np.transpose(pc_array1)
                                    pc_array1 = roi_filter(pc_array1)
                                    intensity_sum1 = 0
                                    count1 = 0
                                    for row in pc_array1:
                                        if row[3] == 6.0:
                                            count1 += 1
                                            intensity_sum1 += row[4]
                                    average_intensity1 = 0
                                    if count > 0:
                                        average_intensity1 = intensity_sum1 / count1
                                    print(filepath_clear)
                                    print(average_intensity1)
                                    print(min_distance)
                                    print(rain_rate)
                                    changed_fraction =  math.exp(-2 * 0.01 * average_distance * math.pow(rain_rate, 0.6)) - 1.0
                                    print(changed_fraction)
                                    predicted_intensity = average_intensity1 * changed_fraction + average_intensity1
                                df = df._append({'File Name': filename, 'Sensor Type': sensor_type, 
                                                 'Rain rate': rain_rate, 
                                                 'Vehicle Detected Points': count, 'Distance to vehicle': min_distance,
                                                 'Average Distance': average_distance, 
                                                 'Average intenisty for vehicle point': average_intensity,
                                                 'Predicted intensity': predicted_intensity
                                                }, ignore_index=True)

    # Write DataFrame to Excel
    df.to_excel(output_excel, index=False)
    print(f"Excel file created at: {output_excel}")
# Example usage:
root_directory = 'output_data_new/0-10'
output_excel = 'intensity_comparison.xlsx'
process_files_and_create_excel(root_directory, output_excel)
