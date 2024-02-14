import cv2
import os
import csv
import collections
import numpy as np

#class to accept data from csv to turn into usable data 
class cell_dat:
    def __init__(self, frame, pos_x, pos_y, velocity_x, velocity_y):
        self.frame = frame
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

#function to input given csv file
#returns dictionary of integer keys and list of cell dat objects
def csv_scanner(file_name):
    class cell_dat:
        def __init__(self, pos_x, pos_y, velocity_x, velocity_y):
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y

    #dictionary of access frame key and list of cell_dat object values
    frame_cell_dict = collections.defaultdict(list)

    with open(file_name) as file_obj:
        #takes in first line of csv file as header
        heading = next(file_obj)

        #creates line by line iterator for csv file
        reader_obj = csv.reader(file_obj)

        #for every row in file, add cell_dat object to list of objects at given frame in a dictionary
        for row in reader_obj:
            template_cell_dat = cell_dat(
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8])
            )
            frame_cell_dict[int(row[1])].append(template_cell_dat)
    print("scan complete")
    return frame_cell_dict
    


#setting parameters for video
#tells program where to source its images from
image_folder = 'A_01fld01'

#customizes output information for the video
video_name = 'plain.mp4' 
fps = 10
dot_color = (0,255,0)
line_color = (0,0,255)

#tells program where to find csv info
csv_folder = "csv_files"
raw_csv_file = "spots_velocity.csv"



#gathers csv data into dictionaries
cell_data_dict = csv_scanner(os.path.join(csv_folder, raw_csv_file))

#collect set of images from given folder and stores quantity of pictures saved
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
image_qt = len(images)

#saves one individual frame to pull width and height of frame from
frame = cv2.imread(os.path.join(image_folder, images[0]))
width = frame.shape[1]
height = frame.shape[0]

#initializes video to add images to
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video = cv2.VideoWriter(video_name, fourcc, fps, (width,height))

#go through every image in the folder
for image_num in range(image_qt):
    #generate name for given folder
    image_name = str(image_num) + ".jpg"

    #open image for drawing points on
    img = cv2.imread(os.path.join(image_folder, image_name),cv2.IMREAD_COLOR)

    #for every object in a given frame
    
    for item in cell_data_dict[image_num]:  
        #parameters: image, center of circle, radius, color, thickness
        cell_coords = (int(item.pos_x), int(item.pos_y))
        cell_predict = ((int(item.pos_x)+int(item.velocity_x)), (int(item.pos_y)+int(item.velocity_y)))
        cv2.line(img, cell_coords, cell_predict, line_color, 5)
        cv2.circle(img, cell_coords, 5, dot_color, -1)
    
    cv2.imwrite('marked/marked_'+ image_name ,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    video.write(cv2.imread(os.path.join('marked', 'marked_'+ image_name)))

cv2.destroyAllWindows()
video.release()

print("Video has been created!")