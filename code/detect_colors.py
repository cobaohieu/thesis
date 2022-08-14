#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Camera Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
# import OpenGL.GL
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
import numpy as np
import numpy.linalg
import sys
import cv2
import datetime
import time
from collections import deque
import copy
import argparse
import tkinter as tk

from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan

global stream
date_and_time = datetime.now()
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

def detect_color(stream):
    # Capturing video through webcam
    # stream = cv2.VideoCapture(0)
 
    # stream.set(cv2.CAP_PROP_FOURCC ,cv2.VideoWriter_fourcc(*'MJPG'))
    codec = 0x47504A4D
    stream.set(cv2.CAP_PROP_FPS, 10)
    stream.set(cv2.CAP_PROP_FOURCC, codec)
    stream.set(3, 1280)
    stream.set(4, 720)

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    FpsCalc = FpsCalculator(buffer_len = 50)

    # Get date and time
    today = str(date_and_time.strftime("%Y-%m-%d %H:%M:%S"))

    # Start a while loop
    while(1):
        display_fps = round(FpsCalc.get(), 3)
        print("FPS: ", display_fps)
        # Reading the video from the
        # webcam in image frames
        _, frame = stream.read()

        # Convert the frame in
        # BGR(RGB color space) to
        # HSV(hue-saturation-value)
        # color space
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Set range for black color and
        # define mask
        black_lower = np.array([0, 0, 0],np.uint8)
        black_upper = np.array([180, 255, 30],np.uint8)
        black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)

        # Set range for white color and
        # define mask
        white_lower = np.array([159, 50, 70], np.uint8)
        white_upper = np.array([180, 255, 255], np.uint8)
        white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

        # Set range for red color and
        # define mask
        red_lower = np.array([0, 0, 231], np.uint8)
        red_upper = np.array([180, 18, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        red2_lower = np.array([0, 50, 70], np.uint8)
        red2_upper = np.array([9, 255, 255], np.uint8)
        red2_mask = cv2.inRange(hsvFrame, red2_lower, red2_upper)

        # Set range for green color and
        # define mask
        green_lower = np.array([36, 50, 70], np.uint8)
        green_upper = np.array([89, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        # Set range for blue color and
        # define mask
        blue_lower = np.array([90, 50, 70], np.uint8)
        blue_upper = np.array([128, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        # Set range for yellow color and
        # define mask
        yellow_lower = np.array([25, 50, 70],np.uint8)
        yellow_upper = np.array([35, 255, 255],np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

        # Set range for purple color and
        # define mask
        purple_lower = np.array([129, 50, 70],np.uint8)
        purple_upper = np.array([158, 255, 255],np.uint8)
        purple_mask = cv2.inRange(hsvFrame, purple_lower, purple_upper)

        # Set range for orange color and
        # define mask
        orange_lower = np.array([10, 50, 70],np.uint8)
        orange_upper = np.array([24, 255, 255],np.uint8)
        orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

        # Set range for gray color and
        # define mask
        gray_lower = np.array([0, 0, 40], np.uint8)
        gray_upper = np.array([180, 18, 230], np.uint8)
        gray_mask = cv2.inRange(hsvFrame, gray_lower, gray_upper)

        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between frame and mask determines
        # to detect only that particular color
        kernal = np.ones((3, 3), "uint8")

        # For black color
        black_mask = cv2.dilate(black_mask, kernal)
        res_black = cv2.bitwise_and(frame, frame,
                                    mask = black_mask)

        # For white color
        white_mask = cv2.dilate(white_mask, kernal)
        res_white = cv2.bitwise_and(frame, frame,
                                    mask = white_mask)

        # For red color
        red_mask = cv2.dilate(red_mask, kernal)
        res_red = cv2.bitwise_and(frame, frame,
                                mask = red_mask)

        red2_mask = cv2.dilate(red2_mask, kernal)
        res_red2 = cv2.bitwise_and(frame, frame,
                                mask = red2_mask)

        # For green color
        green_mask = cv2.dilate(green_mask, kernal)
        res_green = cv2.bitwise_and(frame, frame,
                                    mask = green_mask)

        # For blue color
        blue_mask = cv2.dilate(blue_mask, kernal)
        res_blue = cv2.bitwise_and(frame, frame,
                                    mask = blue_mask)

        # For yellow color
        yellow_mask = cv2.dilate(yellow_mask, kernal)
        res_yellow = cv2.bitwise_and(frame, frame,
                                    mask = yellow_mask)
                                    
        # For purple color
        purple_mask = cv2.dilate(purple_mask, kernal)
        res_purple = cv2.bitwise_and(frame, frame,
                                    mask = purple_mask)

        # For orange color
        orange_mask = cv2.dilate(orange_mask, kernal)
        res_orange = cv2.bitwise_and(frame, frame,
                                    mask = orange_mask)

        # For gray color
        gray_mask = cv2.dilate(gray_mask, kernal)
        res_gray = cv2.bitwise_and(frame, frame,
                                    mask = gray_mask)

        # Creating contour to track black color
        contours, hierarchy = cv2.findContours(black_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (0, 0, 0), 2)
                cv2.putText(frame, "Black Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 0), 2)

        # Creating contour to track white color
        contours, hierarchy = cv2.findContours(white_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (255, 255, 255), 2)
                cv2.putText(frame, "White Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)

        # Creating contour to track red color
        contours, hierarchy = cv2.findContours(red_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (0, 0 ,213), 2)

                cv2.putText(frame, "Red Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0 ,213), 2)

        contours, hierarchy = cv2.findContours(red2_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (0, 0 ,213), 2)

                cv2.putText(frame, "Red Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0 ,213), 2)

        # Creating contour to track green color
        contours, hierarchy = cv2.findContours(green_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (0, 230, 118), 2)

                cv2.putText(frame, "Green Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 230, 118), 2)

        # Creating contour to track blue color
        contours, hierarchy = cv2.findContours(blue_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (255, 145, 0), 2)

                cv2.putText(frame, "Blue Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 145, 0), 2)

        # Creating contour to track orange color
        contours, hierarchy = cv2.findContours(orange_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (41, 121, 255), 2)
                cv2.putText(frame, "Orange Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (41, 121, 255), 2)

        # Creating contour to track yellow color
        contours, hierarchy = cv2.findContours(yellow_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (59, 234, 255), 2)
                cv2.putText(frame, "Yellow Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 234, 255), 2)

        # Creating contour to track purple color
        contours, hierarchy = cv2.findContours(purple_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (255, 235, 59), 2)
                cv2.putText(frame, "Purple Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 235, 59), 2)
        

        # Creating contour to track gray color
        contours, hierarchy = cv2.findContours(gray_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y),
                                        (x + w, y + h),
                                        (158, 158, 158), 2)

                cv2.putText(frame, "Gray Color", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (158, 158, 158), 2)
        
        # puting the FPS count on the frame and display date and time
        cv2.rectangle(frame, (width-640, 2), (81, 21), (0, 0, 0), -1)
        cv2.rectangle(frame, (width-640, 35), (149, 18), (0, 0, 0), -1)

        cv2.putText(frame, "FPS: " + str(display_fps), ((width-640), 15), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str(today), ((0), 30), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow("Multiple Color Detection Mode", frame)
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            # pixmap = QPixmap.fromImage(img)
            # self.imgLabel.setPixmap(pixmap)
            # self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # Program Termination
        key = cv2.waitKey(1)
        if key == 27:
            break
    stream.release()

# def rgb_color_detect_v2():
#     ap = argparse.ArgumentParser()
#     # ap.add_mutually_exclusive_group("-b", type=int, default=64)

#     ap.add_argument("-v", "--video", help="path to the (optional) video file")
#     ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
#     args = vars(ap.parse_args())

#     lower = {'red':(166, 84, 141), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)}
#     upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}

#     colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}

#     if not args.get("video", False):
#         stream = cv2.VideoCapture(0)
#         stream.set(3, 640)
#         stream.set(4, 480)
#         # stream = VideoStream(src=0).start()

#     else:
#         stream = cv2.VideoCapture(args["video"])

#     while True:
#         (grabbed, frame) = stream.read()
#         if args.get("video") and not grabbed:
#             break

#         frame = imutils.resize(frame, width=640)
#         # frame = cv2.resize(frame, 640)

#         blurred = cv2.GaussianBlur(frame, (11, 11), 0)
#         hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

#         for key, value in upper.items():

#             kernel = np.ones((9,9),np.uint8)
#             mask = cv2.inRange(hsv, lower[key], upper[key])
#             mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#             mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#             cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
#                 cv2.CHAIN_APPROX_SIMPLE)[-2]
#             center = None

#             if len(cnts) > 0:
#                 c = max(cnts, key=cv2.contourArea)
#                 ((x, y), radius) = cv2.minEnclosingCircle(c)
#                 M = cv2.moments(c)
#                 center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

#                 if radius > 0.5:
#                     cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 5)
#                     cv2.putText(frame,key + "color", (int(x-radius), int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)

#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#         # img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
#         # pixmap = QPixmap.fromImage(img)
#         # self.imgLabel.setPixmap(pixmap)
#         # self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#         cv2.imshow("Detect colors mode", frame)

#         # press 'q' to stop the loop
#         key = cv2.waitKey(20)
#         if key == 27:
#             break

#     stream.release()
#     cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_color(stream = cv2.VideoCapture(0, cv2.CAP_V4L2))