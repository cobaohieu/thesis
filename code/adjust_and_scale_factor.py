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
from PIL import Image
from imutils.video import VideoStream

from collections import OrderedDict
from collections import deque



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

def make_64k(stream):
    stream.set(3, 61440)
    stream.set(4, 34560)

def make_16k(stream):
    stream.set(3, 15360)
    stream.set(4, 8640)

def make_8k(stream):
    stream.set(3, 7680)
    stream.set(4, 4320)

def make_4k(stream):
    stream.set(3, 3840)
    stream.set(4, 2160)

def make_2k(stream):
    stream.set(3, 2048)
    stream.set(4, 1080)

def make_1080p(stream):
    stream.set(3, 1920)
    stream.set(4, 1080)

def make_896p(stream):
    stream.set(3, 1600)
    stream.set(4, 896)

def make_720p(stream):
    stream.set(3, 1280)
    stream.set(4, 720)

def make_576i(stream):
    stream.set(3, 1024)
    stream.set(4, 576)

def make_720i(stream):
    stream.set(3, 960)
    stream.set(4, 720)

def make_480i(stream):
    stream.set(3, 864)
    stream.set(4, 480)

def make_600i(stream):
    stream.set(3, 800)
    stream.set(4, 600)

def make_448i(stream):
    stream.set(3, 800)
    stream.set(4, 448)

def make_480p(stream):
    stream.set(3, 640)
    stream.set(4, 480)

def make_360p(stream):
    stream.set(3, 640)
    stream.set(4, 360)

def make_288i(stream):
    stream.set(3, 352)
    stream.set(4, 288)

def make_240p(stream):
    stream.set(3, 320)
    stream.set(4, 240)

def make_180i(stream):
    stream.set(3, 320)
    stream.set(4, 180)

def make_144p(stream):
    stream.set(3, 176)
    stream.set(4, 144)

def make_120p(stream):
    stream.set(3, 160)
    stream.set(4, 120)

def make_90i(stream):
    stream.set(3, 160)
    stream.set(4, 90)

def change_res(stream, width, height):
    stream.set(3, width)  # CAP_PROP_FRAME_WIDTH = 3
    stream.set(4, height) # CAP_PROP_FRAME_HEIGHT = 4
                           # CV_CAP_PROP_POS_FRAMES: 0-based index of the frame to be decoded/captured next.
def adjust(stream):
    make_720p(stream)
    change_res(1280, 720)

def rescale_frame(stream, frame, percent=75):
    width  = int((stream.get(cv2.CAP_PROP_FRAME_WIDTH)) * percent/ 100)
    height = int((stream.get(cv2.CAP_PROP_FRAME_HEIGHT)) * percent/ 100)
    dim = (width, height)
    resize = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    return resize

def main_rescale(stream):
    make_576i(stream)

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    FpsCalc = FpsCalculator(buffer_len = 50)
    width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))

    # percent=75
    if (stream.isOpened() == False):
        print('Error while trying to open camera. Plese check again...')

    while True:
        display_fps = round(FpsCalc.get(), 3)
        # Capture frame by frame
        rect, frame = stream.read()

        frame75 = rescale_frame(stream, frame, percent=75)
        frame150 = rescale_frame(stream, frame, percent=150)
        frame200 = rescale_frame(stream, frame, percent=200)

        # puting the FPS count on the frame
        cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
                    font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        # Display resolution frame
        # cv2.imshow('frame75', frame75)
        # cv2.imshow('frame150', frame150)
        # cv2.imshow('frame200', frame200)
        cv2.imshow('Adjust and scale factor mode', frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    stream.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main_rescale(stream = cv2.VideoCapture(0))


