#!/usr/bin/env python
# coding: utf-8

# ## Human Detection with Computer Vision

# In[4]:


import cv2
import imutils
import numpy as np
import argparse


# In[9]:


#We will use HOGDescriptor with SVM already implemented in OpenCV.  Below code will do this work
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#Here, the actual magic will happen
#We call these images as Frame. So in general we will detect the person in the frame. 
#And show it one after another that it looks like a video.

def detect(frame):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frame)

    return frame

#Now, For each Frame, we will call detect() method. Then we write the frame in our output file.

def detectByPathVideo(path, writer):

    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while video.isOpened():
        #check is True if reading was successful 
        check, frame =  video.read()

        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            frame = detect(frame)
            
            if writer is not None:
                writer.write(frame)
            
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()

# DetectByCamera() method

def detectByCamera(writer):   
    video = cv2.VideoCapture(0)
    print('Detecting people...')

    while True:
        check, frame = video.read()

        frame = detect(frame)
        if writer is not None:
            writer.write(frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()


# ## HumanDetector() method

# So our method will check if a path is given then search for the video in the given path and operate.
# Otherwise, it will open the webCam.

# There are two ways of getting Video.
# 1. Web Camera
# 2. Path of file stored

def humanDetector(args):
   # image_path = args["image"]
    video_path = args['video']
    if str(args["camera"]) == 'true' : camera = True 
    else : camera = False

    writer = None
    if args['output'] is not None and image_path is None:
        writer = cv2.VideoWriter(args['output'],cv2.VideoWriter_fourcc(*'MJPG'), 10, (600,600))

    if camera:
        print('[INFO] Opening Web Cam.')
        detectByCamera(writer)
    elif video_path is not None:
        print('[INFO] Opening Video from path.')
        detectByPathVideo(video_path, writer)


# ## Argparse() method

# In[ ]:


#The function argparse() simply parses and returns as a dictionary the arguments passed through your terminal to our script. 
#There will be Two arguments within the Parser for this project:
# 1. Video: The path to the Video file inside your system
# 2. Camera: A variable that if set to ‘true’ will call the cameraDetect() method

def argsParser():
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video", default=None, help="path to Video File ")
    arg_parse.add_argument("-i", "--image", default=None, help="path to Image File ")
    arg_parse.add_argument("-c", "--camera", default=False, help="Set true if you want to use the camera.")
    arg_parse.add_argument("-o", "--output", type=str, help="path to optional output video file")
    args = vars(arg_parse.parse_args())

    return args


# In[10]:


if __name__ == "__main__":
 HOGCV = cv2.HOGDescriptor()
 HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

 args = argsParser()
 humanDetector(args)

##this program can only be run in the python terminal
# for video imput run this code below
# python main.py -v 'path_to_video"
# for camera
#python main.py -c true