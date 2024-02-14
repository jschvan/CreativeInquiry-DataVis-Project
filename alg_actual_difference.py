import cv2
import os
import csv #can i delete?
import pandas as pd
import collections
import numpy as np

class cell_dat:
    def __init__(self, pos_x, pos_y, velocity_x, velocity_y, velocity_x_12, velocity_y_12):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_x_12 = velocity_x_12
        self.velocity_y_12 = velocity_y_12

def csv_scanner(file_name):
    #create pandas dataframe from csv file
    pandas_df = pd.read_csv(file_name)

    #dictionary with frame key and list of cell_dat object values
    frame_cell_dict = collections.defaultdict(list)

    for index, row in pandas_df.iterrows():
        key = row['FRAME']
        template_cell_dat = cell_dat(
            row['pos_x'],
            row['pos_y'],
            row['dt1_n0_dx'],
            row['dt1_n0_dy'],
            row['dt12_n0_dx'],
            row['dt12_n0_dy']
        )
        frame_cell_dict[key].append(template_cell_dat)
    print("scan complete for " + file_name)
    return frame_cell_dict

#setting parameters for video
#tells program where to source its images from
image_folder = 'A_01fld01'

#tells program where to find csv info
csv_folder = "csv_files"
raw_csv_file = "spots_velocity.csv"
alg_csv_file = "A_01fld01.csv"
interval = 12

#gathers csv data into dictionaries
cell_data_dict = csv_scanner(os.path.join(csv_folder, raw_csv_file))
alg_data_dict = csv_scanner(os.path.join(csv_folder, alg_csv_file))

#runs through number in range
#does this as opposed to looping through every image in folder
#could this be fixed?

image_qt = len(cell_data_dict.keys())
print(image_qt)
for image_count in range(image_qt):
    if image_count % interval or image_count == 0:
        for data, alg in cell_data_dict[image_count], alg_data_dict[image_count/interval]:
            real_x_vel_12 = data.velocity_x_12
            real_y_vel_12 = data.velocity_y_12
            alg_x_vel_12 = alg.velocity_x_12
            alg_y_vel_12 = alg.velocity_y_12

            print("Difference in X: " + real_x_vel_12 - alg_x_vel_12)
            print("Difference in Y: " + real_y_vel_12 - alg_y_vel_12)
        

