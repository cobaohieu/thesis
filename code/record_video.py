#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Module

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
import sys
import cv2
import os
import datetime
import time
import imutils
import numpy as np
import numpy.linalg

################## Import sub modules ##################
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from PIL import Image
from imutils.video import VideoStream

from collections import OrderedDict
from collections import deque
from multiprocessing.pool import ThreadPool

frames_per_second = 24
res = '720p'
# res = '480p'
# width = 1280
global stream
extension = 'avi'
# stream = cv2.VideoCapture(0)
username = os.getlogin()
filename_linux = '/home/'+username+'/Pictures/C922/VID_'+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.mp4'
filename_win = 'C:/Users/administrator/Pictures/C922/VID_'+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.mp4'


################## FPS Calculator ##################
class FpsCalculator(object):
    def __init__(self, buffer_len = 1):
        self._start_tick = cv2.getTickCount()
        self._freq = 1000.0 / cv2.getTickFrequency()
        self._difftimes = deque(maxlen = buffer_len)

    def get(self):
        current_tick = cv2.getTickCount()
        different_time = (current_tick - self._start_tick) * self._freq
        self._start_tick = current_tick

        self._difftimes.append(different_time)

        fps = 1000.0 / (sum(self._difftimes) / len(self._difftimes))
        fps_rounded = round(fps, 3)

        return fps_rounded

def set_file_name(ext=extension):
    path = '/home/jetson/Videos/C922/VID_'
    time = str(strftime("%Y-%b-%d at %H.%M.%S %p"))
    ext = ext
    filename = path+time+'.'+ext
    return filename

def change_res(stream, width, height):
    stream.set(3, width)
    stream.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
    "96p" : (128, 96),        # 4:3
    "120p" : (160, 122),      # 4:3
    "144p" : (176, 144),      # 11:9 | 256×144 16:9
    "240p" : (320, 240),      # 4:3  | 426×240 16:9
    "360p" : (640, 360),      # 4:3  | 640×360 16:9
    "480p" : (720, 480),
    "540p" : (960, 549),
    "720p" : (1280, 720),
    "1080p": (1920, 1080),
    "1440p": (2560, 1440),
    "2k"   : (2048, 1080),    # (3840, 2160),
    "4k"   : (3840, 2160),
    "8k"   : (7680, 4320),
    "16k"  : (15360, 8640),
    "64k"  : (61440, 34560)}

# grab resolution dimensions and set video capture to it.
def get_dims(stream, res=res):
    width, height = STD_DIMENSIONS["720p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    change_res(stream, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    # 'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'avi': cv2.VideoWriter_fourcc(*'DIVX'),
    # 'avi': cv2.VideoWriter_fourcc(*'WMV1'),
    # 'avi': cv2.VideoWriter_fourcc(*'WMV2'),
    'avi': cv2.VideoWriter_fourcc('M','J','P','G'),
    # 'mp4': cv2.VideoWriter_fourcc(*'MJPG'),
    # 'mp4': cv2.VideoWriter_fourcc('M','J','P','G'),
    # 'mp4': cv2.VideoWriter_fourcc(*'X264'),
    # 'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    'mkv': cv2.VideoWriter_fourcc(*'X264')}

def video_type(type):
    type = {
        'avi': cv2.VideoWriter_fourcc(*'DIVX'),
        # 'avi': cv2.VideoWriter_fourcc(*'XVID'),
        'avi': cv2.VideoWriter_fourcc('M','J','P','G'),
        'mkv': cv2.VideoWriter_fourcc(*'X264'),
        # 'mp4': cv2.VideoWriter_fourcc(*'MPEG'),
        # 'mp4': cv2.VideoWriter_fourcc(*'MP4V'),
        # 'mp4': cv2.VideoWriter_fourcc(*'XVID'),
        }
#     return type

    
# VIDEO_TYPE[
#         'avi': cv2.VideoWriter_fourcc(*'DIVX'),
#         # 'avi': cv2.VideoWriter_fourcc(*'XVID'),
#         'avi': cv2.VideoWriter_fourcc('M','J','P','G'),
#         'mkv': cv2.VideoWriter_fourcc(*'X264')
#         # 'mp4': cv2.VideoWriter_fourcc(*'MPEG'),
#         # 'mp4': cv2.VideoWriter_fourcc(*'MP4V'),
#         # 'mp4': cv2.VideoWriter_fourcc(*'XVID'),
#     ]


def get_video_type_v2(filename=filename_linux):
    filename, ext = os.path.splitext(filename)
    if ext in video_type:
        return  video_type([ext])
    return video_type(['avi'])

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']
    # return VIDEO_TYPE['mp4']
    # return VIDEO_TYPE['mkv']

def get_video_type(ext=extension):
    if ext in VIDEO_TYPE:
        return  VIDEO_TYPE[ext]
    # return VIDEO_TYPE['avi']
    # return VIDEO_TYPE['mp4']
    # return VIDEO_TYPE['mkv']

def put_text_on_video(frame, fps, time):
    # set font for display
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Get date and time
    date_and_time = datetime.now() 
    today = str(date_and_time.strftime("%Y-%m-%d %H:%M:%S"))

    # puting the FPS count on the frame and display date and time
    box_time = cv2.rectangle(frame, (0, 3), (149, 18), (0, 0, 0), -1)        
    box_fps = cv2.rectangle(frame, (0, 35), (81, 18), (0, 0, 0), -1)

    text_time = cv2.putText(frame, str(today), ((0), 15), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    text_fps = cv2.putText(frame, "FPS: " + str(fps), ((0), 30), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

    return box_time, box_fps, text_time, text_fps

def record(stream, filename=set_file_name(), frames_per_second=frames_per_second, res=res):
    if not stream.isOpened() or (stream.isOpened() == False):
        print("Unable to open camera")
        exit()
        # sys.exit()

    stream.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc(*'MJPG'))
    stream.set(cv2.CAP_PROP_FPS, frames_per_second)

    # stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))

    FpsCalc = FpsCalculator(buffer_len = 50)
    count = 0
    out = cv2.VideoWriter(filename, get_video_type(filename), frames_per_second, get_dims(stream, res))

    # while True:
    while stream.isOpened():
        count = count + 1
        fps = round(FpsCalc.get(), 3)
        print(fps)
        # Read and display each frame
        (ret, frame) = stream.read()
        
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
            # sys.exit()

        frame = cv2.flip(frame, 1)
        # puting the FPS count on the frame and display date and time
        put_text_on_video(frame, fps, time)
        cv2.imshow("Record video mode", frame)

        key = cv2.waitKey(1) & 0xFF
        # Specify the countdown
        j = 30
        # set the key for the countdown to begin
        if key == ord('q'):
            while j>=10:
                (ret, frame) = stream.read()
                frame = cv2.flip(frame, 1)

                # Display the countdown after 10 frames so that it is easily visible otherwise,
                # it will be fast. You can set it to anything or remove this condition and put 
                # countdown on each frame
                if j%10 == 0:
                    # specify the font and draw the countdown using puttext
                    font = cv2.FONT_HERSHEY_SIMPLEX

                    # get coords based on boundary
                    textX = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH) / 2.5)
                    textY = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT) / 1.35)
                    cv2.putText(frame, str(j//10), (textX, textY), font, 15, (255,255,255), 10, cv2.LINE_AA)

                # puting the FPS count on the frame and display date and time
                put_text_on_video(frame, fps, time)

                cv2.imshow("Record video mode", frame)
                cv2.waitKey(125)
                j = j-1
            else:
                (ret, frame) = stream.read()
                frame = cv2.flip(frame, 1)
                # Display the clicked frame for 1 sec.
                # You can increase time in waitKey alsoE_AA)

                # puting the FPS count on the frame and display date and time
                put_text_on_video(frame, fps, time)
                out.write(frame)
                cv2.imshow("Record video mode", frame)
                cv2.waitKey(1)

        # Pause the camera
        if key == 32:
            cv2.waitKey()
        # Stop the camera
        elif key == 27:
            break

    stream.release()
    out.release()
    # cv2.destroyAllWindows()

def open_camera():
    # yuck - opencv has no way to count # of cameras, so do this hack of looking for /dev/video*
    numCameras = len(filter(lambda s: s.startswith("video"), os.listdir("/dev")))
 
    c = cv2.VideoCapture()
    # We start our search with higher numbered (likely external) cameras
    for cnum in range(0, numCameras):
        c.open(numCameras - cnum - 1)
        if c.isOpened():
            return c
 
    raise Exception('No cameras found')

# def init_camera(self):
#     # return immediately if already initialised
#     if not self.camera is None:
#         return
 
#     # use webcam
#     if self.camera_type == 0:
#         self.camera = cv2.VideoCapture(0)
#         #self.camera.set(cv2.cv2.CV_CAP_PROP_FRAME_WIDTH,self.img_width)
#         #self.camera.set(cv2.cv2.CV_CAP_PROP_FRAME_HEIGHT,self.img_height)
 
#         # check we can connect to camera
#         if not self.camera.isOpened():
#             print "failed to open camera, exiting!"
#             sys.exit(0)
 
#     # use rpi camera
#     if self.camera_type == 1:
#         self.camera = PiCamera()
#         self.camera.resolution = (self.img_width,self.img_height)
	
def open_file(self):
    self.video = cv2.VideoCapture(self.file_name)

def getInfo(sourcePath):
    cap = cv2.VideoCapture(sourcePath)
    info = {
        "framecount": cap.get(cv2.CV_CAP_PROP_FRAME_COUNT),
        "fps": cap.get(cv2.CV_CAP_PROP_FPS),
        "width": int(cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT)),
        "codec": int(cap.get(cv2.CV_CAP_PROP_FOURCC))
    }
    cap.release()
    return info

def process_frame(frame):
    # some intensive computation...
    # frame = cv2.medianBlur(frame, 19)
    return frame

def open_cam_rtsp(uri, width, height, latency):
    gst_str = ("rtspsrc location={} latency={} ! rtph264depay ! h264parse ! omxh264dec ! "
               "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
               "videoconvert ! appsink").format(uri, latency, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def open_cam_usb(dev=0, width=1280, height=720):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ("v4l2src device=/dev/video{} ! "
               "video/x-raw, width=(int){}, height=(int){}, format=(string)RGB ! "
               "videoconvert ! appsink").format(dev, width, height)      
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

def open_cam_onboard(width, height):
    # On versions of L4T previous to L4T 28.1, flip-method=2
    # Use Jetson onboard camera
    gst_str = ("nvcamerasrc ! "
               "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458, format=(string)I420, framerate=(fraction)30/1 ! "
               "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
               "videoconvert ! appsink").format(width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

if __name__ == "__main__":
    record(stream = cv2.VideoCapture(0, cv2.CAP_V4L2))
    # record(stream = cv2.VideoCapture(1), frames_per_second=30, filename=filename_win, res="480")
    # v4l2src device=/dev/video0 io-mode=2 ! image/jpeg, width=3264,height=2448,framerate=20/1 ! jpegparse ! jpegdec ! videoconvert ! video/x-raw,width=3264,height=2448,format=BGR ! appsink
    # print(cv2.CAP_FFMPEG)
    # print(cv2.CAP_GSTREAMER)
    # print(cv2.CAP_INTEL_MFX)
    # print(cv2.CAP_V4L2)
    # print(cv2.CAP_V4L)
    # print(cv2.CAP_IMAGES)
    # print(cv2.CAP_MJPEG)
    # get_fps(stream = cv2.VideoCapture(0))
