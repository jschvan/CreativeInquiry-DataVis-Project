import cv2
import os
import csv #can i delete?
import pandas as pd
import collections
import numpy as np
from queue import Queue

parent_directory = os.path.join(os.getcwd(), "..")

#setting parameters for video
#tells program where to source its images from
image_folder = 'references/A_01fld01'

#customizes output information for the video
frame_count = 
video_name = str(frame_count) + '_frame_plain.mp4' 
fps = 1

#collect set of images from given folder and stores quantity of pictures saved
images = [img for img in os.listdir(os.path.join(parent_directory, image_folder)) if img.endswith(".jpg")]
image_qt = len(images)

#saves one individual frame to pull width and height of frame from
frame = cv2.imread(os.path.join(parent_directory + '/' + image_folder, images[0]))
width = frame.shape[1]
height = frame.shape[0]

#initializes video to add images to
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(os.path.join('../output/output_videos', video_name), fourcc, fps, (width,height))


loop_count = 0

for image_num in range(image_qt): 

    #generate name for image to be found
    image_name = str(image_num) + ".jpg"
    if image_num % frame_count == 0:
        video.write(cv2.imread(parent_directory + '/' + image_folder + '/' + image_name))

cv2.destroyAllWindows()
video.release()

print("Video has been created!")