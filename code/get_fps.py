#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Camera Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
from __future__ import print_function
from math import radians, degrees, cos, sin, tan
# import OpenGL.GL
import numpy as np
import numpy.linalg
import sys
import os
import cv2
import datetime
import time
import copy
import PIL
import argparse
import imutils
import logging
import tkinter as tk
import mss
import multiprocessing
import colorsys
import random

################## Import sub modules ##################
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from PIL import Image
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from screeninfo import get_monitors

# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *

from collections import OrderedDict
from collections import deque


from collect_XLM_images import *


width = 640
height = 480

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

def set_default_fps(stream):
    # font which we will be using to display FPS
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # FpsCalc = FpsCalculator(buffer_len = 1)

    # Start default stream
    # stream = cv2.VideoCapture(0)
    length = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Length: ", length)
    width  = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Width: ", width)
    height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Height: ", height)
    fps    = stream.get(cv2.CAP_PROP_FPS)
    print("FPS: ", fps)

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    if int(major_ver)  < 3 :
        fps = stream.get(cv2.cv.CV_CAP_PROP_FPS)
        # self.plainTextEdit.setPlainText("Frames per second using stream.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        print("Frames per second using stream.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    else :
        fps = stream.get(cv2.CAP_PROP_FPS)
        # self.plainTextEdit.setPlainText(str("Frames per second using stream.get(cv2.CAP_PROP_FPS) : {0}".format(fps)))
        print("Frames per second using stream.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Number of frames to capture
    num_frames = 480;

    # self.plainTextEdit.setPlainText(str("Capturing {0} frames".format(num_frames)))
    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    # Grab a few frames
    for i in range(0, num_frames) :
        # display_fps = round(FpsCalc.get(), 3)
        # self.plainTextEdit.setPlainText(str("FPS: {0}".format(display_fps)))
        # print("FPS: {0}".format(display_fps))

        ret, frame = stream.read()
        frame = imutils.resize(frame, width=640, height=480)

        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap.fromImage(img)
        # self.imgLabel.setPixmap(pixmap)
        # self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # puting the FPS count on the frame
        # cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
        #             font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        # show the output frame
        # cv2.imshow('Get Frame', frame)

        # if the `ESC` key was pressed, break from the loop
        key = cv2.waitKey(100)
        if key == 27:
            break
    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    # self.plainTextEdit.setPlainText(str("Time taken : {0} seconds".format(seconds)))
    print("Time taken : {0} seconds".format(seconds))
    # print("FPS: {0}".format(display_fps))

    # Calculate frames per second
    fps  = num_frames / seconds
    # self.plainTextEdit.setPlainText(str("Estimated frames per second : {0}".format(fps)))
    print("Estimated frames per second : {0}".format(fps))
    # print("FPS: {0}".format(display_fps))

    # Release video
    stream.release()
    cv2.destroyAllWindows()

def set_default_fps_v2():
    curr_time = time.time()
    stream = cv2.VideoCapture(0)

    FpsCalc = FpsCalculator(buffer_len = 120)

    def wait(delay):
        # capture and discard frames while the delay is not over
        while time.time()-curr_time < delay:
            stream.read()

    while True:
        display_fps = round(FpsCalc.get(), 3)
        # select and wait random delay time
        delay = random.random()
        wait(delay)

        # update curr_time
        curr_time = time.time()

        # get and display next frame
        ret, frame = stream.read()
        # frame = imutils.resize(frame, width=640, height=480)
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap.fromImage(image)
        # self.imgLabel.setPixmap(pixmap)
        # self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # font which we will be using to display FPS
        font = cv2.FONT_HERSHEY_SIMPLEX

        # puting the FPS count on the frame
        cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
                    font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Get FPS mode", frame)
        key = cv2.waitKey(100) & 0xFF
        if key == 27:
            stream.release()
            break
    stream.release()
    cv2.destroyAllWindows()

def increase_fps():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--num-frames", type=int, default=240,
    help="# of frames to loop over for FPS test")
    ap.add_argument("-d", "--display", type=int, default=-1,
    help="Whether or not frames should be displayed")
    args = vars(ap.parse_args())

    # grab a pointer to the video stream and initialize the FPS counter
    print("[INFO] sampling frames from webcam...")
    stream = cv2.VideoCapture(0)

    width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    FpsCalc = FpsCalculator(buffer_len=1)
    fps = FPS().start()

    # loop over some frames
    while fps._numFrames < args["num_frames"]:
        display_fps = round(FpsCalc.get(), 3)
        print("Currently, FPS is: ", display_fps)
        # grab the frame from the stream and resize it to have a maximum
        # width of 400 pixels
        (grabbed, frame) = stream.read()
        frame = imutils.resize(frame, width=480)

        # check to see if the frame should be displayed to our screen
        if args["display"] > 0:

            # puting the FPS count on the frame
            # cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
            #                 font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    stream.release()
    cv2.destroyAllWindows()

    # created a *threaded* video stream, allow the camera sensor to warmup,
    # and start the FPS counter
    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=0).start()
    # width1 = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    FpsCalc1 = FpsCalculator(buffer_len=1)
    fps = FPS().start()

    # loop over some frames...this time using the threaded stream
    while fps._numFrames < args["num_frames"]:
        display_fps1 = round(FpsCalc1.get(), 0)
        print("Currently, FPS is: ", display_fps1)
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # check to see if the frame should be displayed to our screen
        if args["display"] > 0:

            # puting the FPS count on the frame
            # cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
            #              font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

if __name__ == "__main__":
    increase_fps()
