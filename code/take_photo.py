#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Pixy Application V2020

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
# from PIL import Image
# from imutils.video import VideoStream
from collections import OrderedDict
from collections import deque

global stream
username = os.getlogin()
date_and_time = datetime.now()
filename = '/home/'+username+'/Pictures/C922/IMG_'+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
width = 640
height = 480
# stream = cv2.VideoCapture(0)

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

def change_res(stream, width, height):
    stream.set(3, width)
    stream.set(4, height)

def save_frame(image):
    jpgfile = time.strftime("%Y%m%d-%H%M%S.jpg")
    savefile = image_path + f"\\{jpgfile}"
    cv2.imwrite(savefile, image)
    file = pathlib.Path(savefile)
    if file.exists():
        print("File saved")
    else:
        print("File NOT saved!")

def capture(stream, filename=filename, width=width):
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    FpsCalc = FpsCalculator(buffer_len = 50)
    # codec = 0x47504A4D 
    # stream.set(cv2.CAP_PROP_FPS, 30.0)
    # stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
    # stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
    # stream.set(cv2.CAP_PROP_FOURCC, codec)
    # stream.set(3, 1280)
    # stream.set(4, 720)
    change_res(stream, width, height)
    count = 0

    # Get date and time
    today = str(date_and_time.strftime("%Y-%m-%d %H:%M:%S"))

    while True:
        count = count + 1
        display_fps = round(FpsCalc.get(), 3)
        print("FPS: ", display_fps)

        (ret, frame) = stream.read()
        # frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame =  cv2.cvtColor(frame, cv2.THRESH_BINARY)
        # frame = cv2.flip(frame, 0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
        # frame =  cv2.bitwise_not(frame)

        # puting the FPS count on the frame and display date and time
        # cv2.rectangle(frame, (0, 2), (81, 21), (0, 0, 0), -1)        
        # cv2.rectangle(frame, (0, 35), (149, 18), (0, 0, 0), -1)

        # cv2.putText(frame, "FPS: " + str(display_fps), ((0), 15), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        # cv2.putText(frame, str(today), ((0), 30), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imwrite(filename.format(count), frame)
        cv2.imshow("Capture image mode", frame)
        key = cv2.waitKey(1)
        print('Image saved as:', filename)
        os.chmod(filename , 0o777)

        # if key == 27 or key == ord('q') or key == ord('Q'):
        if key == 27:
            break

    stream.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    capture(stream = cv2.VideoCapture(0))
