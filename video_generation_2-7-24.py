import cv2
import os
import csv #can i delete?
import pandas as pd
import collections
import numpy as np

class cell_dat:
    def __init__(self, pos_x, pos_y, velocity_x_8, velocity_y_8):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x_8 = velocity_x_8
        self.velocity_y_8 = velocity_y_8

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
            row['dt8_n0_dx'],
            row['dt8_n0_dy']
        )
        frame_cell_dict[key].append(template_cell_dat)
    print("scan complete for " + file_name)
    return frame_cell_dict

#setting parameters for video
#tells program where to source its images from
image_folder = 'A_01fld01'

#customizes output information for the video
video_name = '8__predict+xy_track.mp4' #can we make this mp4?
fps = 7
green = (0,255,0)
red = (0,0,255)
blue = (255, 0, 0)


#tells program where to find csv info
#currently using the cnn_dt8 algorithim
csv_folder = "csv_files"
raw_csv_file = "spots_velocity.csv"
alg_csv_file = "A_01fld01.csv"
interval = 8

#gathers csv data into dictionaries
cell_data_dict = csv_scanner(os.path.join(csv_folder, raw_csv_file))
alg_data_dict = csv_scanner(os.path.join(csv_folder, alg_csv_file))

#collect set of images from given folder and stores quantity of pictures saved
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
image_qt = len(images)

#saves one individual frame to pull width and height of frame from
frame = cv2.imread(os.path.join(image_folder, images[0]))
width = frame.shape[1]
height = frame.shape[0]

#initializes video to add images to
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))

#runs through number in range
#does this as opposed to looping through every image in folder
#could this be fixed?

loop_count = 0
xy_set = []

for image_num in range(image_qt):
    if loop_count == interval:
        loop_count = 0
        xy_set = []

    #generate name for image to be found
    image_name = str(image_num) + ".jpg"

    #open image for drawing points on
    img = cv2.imread(os.path.join(image_folder, image_name),cv2.IMREAD_COLOR)

    #for every object in a given frame
    for item in cell_data_dict[image_num]:  
        #parameters: image, center of circle, radius, color, thickness
        cell_coords = (int(item.pos_x), int(item.pos_y))
        xy_set.append(cell_coords)
        for coords in xy_set:
            cv2.circle(img, coords, 5, green, -1)
        
    '''
    for item in cell_data_dict[image_num-loop_count]:
        cell_coords = (int(item.pos_x), int(item.pos_y))
        cell_velocity = (int(item.pos_x) + int(item.velocity_x_8)), (int(item.pos_y) + int(item.velocity_y_8))  
        cv2.line(img, cell_coords, cell_velocity, green, 5)
    '''  
              

    for item in alg_data_dict[int(image_num/interval)]:  
        #parameters: image, center of circle, radius, color, thickness
        cell_coords = (int(item.pos_x), int(item.pos_y))
        cell_predict = ((int(item.pos_x)+int(item.velocity_x_8)), (int(item.pos_y)+int(item.velocity_y_8)))
        cv2.line(img, cell_coords, cell_predict, red, 5)

    loop_count = loop_count + 1

    cv2.imwrite('marked/marked_'+ image_name ,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    video.write(cv2.imread(os.path.join('marked', 'marked_'+ image_name)))

cv2.destroyAllWindows()
video.release()

print("Video has been created!")