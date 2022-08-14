

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Head       :Camera Application V2020

Description:

Author     : Co Bao Hieu
Id         : M3718007
"""

################## Import Modules ##################
from math import radians, degrees, cos, sin, tan
# import OpenGL.GL
import numpy as np
import numpy.linalg
import os
import sys
import cv2
import time
import pyzbar.pyzbar as pyzbar
import copy
import argparse
import tkinter as tk
import csv

from pyzbar import pyzbar
from pyzbar.pyzbar import decode
from collections import deque
from time import gmtime, strftime
from datetime import datetime
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *


global stream
date_and_time = datetime.now()
width = 640
height = 480

# Identify Timestamp
timestr = time.strftime("%Y%m%d-%H%M%S")

# Load csv
# file_name = 'qr_result.csv'

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

def detect_qr_code(stream):
    # stream = cv2.VideoCapture(0)
    codec = 0x47504A4D
    # stream.set(cv2.CAP_PROP_FPS, 10)
    stream.set(3, 720)
    stream.set(4, 480)

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    FpsCalc = FpsCalculator(buffer_len = 50)

    # Get date and time
    today = str(date_and_time.strftime("%Y-%m-%d %H:%M:%S"))

    # with open(file_name, 'w', encoding='UTF8', newline='') as outfile:
    #     writer = csv.writer(outfile) #, dialect=csv.excel_tab)

    while True:
        display_fps = round(FpsCalc.get(), 3)
        print("FPS: ", display_fps)

        ret, frame = stream.read()
        # if the frame was not ret, then we have reached the end
        # of the stream
        if not ret:
            break

        for barcode in decode(frame):
            text = barcode.data.decode('utf-8')
            print(text) # Skip header row.

            # write a row to the csv file
            # writer.writerow(text)

            # self.plainTextEdit.setPlainText(str(text))
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(frame, text, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # puting the FPS count on the frame and display date and time
        cv2.rectangle(frame, (width-640, 2), (81, 21), (0, 0, 0), -1)
        cv2.rectangle(frame, (width-640, 35), (149, 18), (0, 0, 0), -1)

        cv2.putText(frame, "FPS: " + str(display_fps), ((width-640), 15), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str(today), ((0), 30), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow('Detect QR Code Mode', frame)
        # cv2.waitKey(1)
        # img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        # pixmap = QPixmap.fromImage(img)
        # self.imgLabel.adjustSize()
        # self.imgLabel.setPixmap(pixmap)
        # self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        key = cv2.waitKey(1)
        if key == 27:
            break
            # outfile.close()
        
    stream.release()

# def scan_and_decode_v2(self):
#     self.clear_image()
#     # construct the argument parser and parse the arguments
#     ap = argparse.ArgumentParser()
#     ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
#                     help="path to output CSV file containing barcodes")
#     args = vars(ap.parse_args())
#     # initialize the video stream and allow the camera sensor to warm up
#     self.plainTextEdit.setPlainText(str("[INFO] starting video stream..."))

#     # font which we will be using to display FPS
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     FpsCalc = FpsCalculator(buffer_len = 50)

#     stream = VideoStream(src=0).start()
#     # stream = VideoStream(usePiCamera=True).start()
#     # stream = cv2.VideoCapture(0)
#     time.sleep(2.0)
#     # open the output CSV file for writing and initialize the set of
#     # barcodes found thus far
#     csv = open(args["output"], "w")
#     found = set()

#     # loop over the frames from the video stream
#     while True:
#         display_fps = round(FpsCalc.get(), 3)
#         print(display_fps)

#         # grab the frame from the threaded video stream and resize it to
#         # have a maximum width of 400 pixels
#         frame = stream.read()
#         frame = imutils.resize(frame, width=640)
#         # find the barcodes in the frame and decode each of the barcodes
#         barcodes = pyzbar.decode(frame)
#         for barcode in barcodes:
#             # extract the bounding box location of the barcode and draw
#             # the bounding box surrounding the barcode on the image
#             (x, y, w, h) = barcode.rect
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
#             # the barcode data is a bytes object so if we want to draw it
#             # on our output image we need to convert it to a string first
#             barcodeData = barcode.data.decode("utf-8")
#             barcodeType = barcode.type
#             # draw the barcode data and barcode type on the image
#             text = "{} ({})".format(barcodeData, barcodeType)
#             text = "{}".format(barcodeData)
#             # print(text)
#             self.plainTextEdit.setPlainText(str(text))

#             cv2.putText(frame, text, (x, y - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#             # if the barcode text is currently not in our CSV file, write
#             # the timestamp + barcode to disk and update the set
#             if barcodeData not in found:
#                 pygame.mixer.init()
#                 csv.write("{},{}\n".format(datetime.datetime.now(),
#                     barcodeData))
#                 csv.flush()
#                 found.clear()
#                 found.add(barcodeData)

#         # puting the FPS count on the frame
#         cv2.rectangle(frame, (width-640, 0), (61, 21), (0, 0, 0), -1)
#         cv2.putText(frame, "FPS:"+str(display_fps), ((width-150), 30),
#                     font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

#         # show the output frame
#         cv2.imshow("Barcode Scanner", frame)
#         # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#         # img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
#         # pixmap = QPixmap.fromImage(img)
#         # self.imgLabel.setPixmap(pixmap)
#         # self.imgLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

#         # close the output CSV file do a bit of cleanup
#         self.plainTextEdit.setPlainText(str("[INFO] cleaning up..."))
#         csv.close()
#         stream.stop()
#         key = cv2.waitKey(1)
#         if key == 27:
#             break

if __name__ == "__main__":
    detect_qr_code(stream = cv2.VideoCapture(0, cv2.CAP_V4L2))