import os
import cv2
import datetime
import time
import math
import imutils
import numpy as np
import numpy.linalg

from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from collections import OrderedDict, deque
from PIL import Image
from imutils.video import VideoStream

from collections import OrderedDict, deque
from threading import Thread

def show_fps(frame, fps):
    """Draw fps number at top-left corner of the image."""
    font = cv2.FONT_HERSHEY_PLAIN
    line = cv2.LINE_AA
    fps_text = 'FPS: {:.2f}'.format(fps)
    cv2.putText(frame, fps_text, (11, 20), font, 1.0, (32, 32, 32), 4, line)
    cv2.putText(frame, fps_text, (10, 20), font, 1.0, (240, 240, 240), 1, line)
    return frame

def changeBrightness(x):
    brightness = cv2.getTrackbarPos('brightness',Window_name)
    brightness = (brightness - 0) * 255 / (255 - 0)
    print("Brightness now is:", brightness)
    stream.set(10, brightness)

def changeContrast(x):
    contrast = cv2.getTrackbarPos('contrast',Window_name)
    contrast = (contrast - 0) * 255 / (255 - 0)
    print("Brightness now is:", contrast)
    stream.set(11, contrast)

def changeSaturation(x):
    saturation = cv2.getTrackbarPos('saturation',Window_name)
    saturation = (saturation - 0) * 255 / (255 - 0)
    print("Brightness now is:", saturation)
    stream.set(12,saturation)

def changeGain(x):
    gain = cv2.getTrackbarPos('gain',Window_name)
    gain = (gain - 0) * 255 / (255 - 0)
    print("Brightness now is:", gain)
    stream.set(14,gain)

def changeExposure(x):
    exposure = cv2.getTrackbarPos('exposure',Window_name)
    exposure = (exposure - 0) * 2047 / (2047 - 0)
    print("Brightness now is:", exposure)
    stream.set(15,exposure)

def changeSharpness(x):
    sharpness = cv2.getTrackbarPos('sharpness',Window_name)
    sharpness = (sharpness - 0) * 255 / (255 - 0)
    print("Brightness now is:", sharpness)
    stream.set(20,sharpness)

def changedWhiteBalanceTemperature(self,value):
    white_balance_temperature = cv2.getTrackbarPos('white_balance_temperature',Window_name)
    white_balance_temperature = (value - 0) * 6500 / (6500 - 0)
    self.stream.set(45, white_balance_temperature)

def changeFocus(x):
    focus = cv2.getTrackbarPos('focus',Window_name)
    focus = (focus - 0) * 250 / (250 - 0)
    print("Brightness now is:", focus)
    stream.set(28,focus)

def changeZoom(x):
    zoom = cv2.getTrackbarPos('zoom',Window_name)
    zoom = (zoom - 0) * 500 / (500 - 0)
    print("Brightness now is:", zoom)
    stream.set(27,zoom)

def main(stream, Window_name):
    cv2.namedWindow(Window_name)
    stream.set(cv2.CAP_PROP_SETTINGS, 0)
    stream.set(3,640)
    stream.set(4,480)
    stream.set(5, 30.0)
    
    print("FRAME_WIDTH", stream.get(3))
    print("FRAME_HEIGHT", stream.get(4))
    print("FPS", stream.get(5))
    print("BRIGHTNESS", stream.get(10))
    print("CONTRAST", stream.get(11))
    print("SATURATION", stream.get(12))
    print("GAIN", stream.get(14))
    print("EXPOSURE", stream.get(15))
    print("SHARPNESS", stream.get(20))
    print("FOCUS", stream.get(28))
    print("ZOOM", stream.get(27))

    fps = 0.0
    tic = time.time()

    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # create trackbars for color change
    # get current brightness and contrast values
    brightness = int(round(stream.get(10) * 255))
    contrast = int(round(stream.get(11) * 255))
    saturation = int(round(stream.get(12) * 255))
    gain = int(round(stream.get(14) * 255))
    exposure = int(round(stream.get(15) * 2047))
    sharpness = int(round(stream.get(20) * 255))
    wbtemperature = int(round(stream.get(20) * 6500))
    focus = int(round(stream.get(28) * 250))
    zoom = int(round(stream.get(27) * 500))
    cv2.createTrackbar('Brightness',Window_name,brightness,255,changeBrightness)
    cv2.createTrackbar('Contrast',Window_name,contrast,255,changeContrast)
    cv2.createTrackbar('Saturation',Window_name,saturation,255,changeSaturation)
    cv2.createTrackbar('Gain',Window_name,gain,255,changeGain)
    cv2.createTrackbar('Exposure',Window_name,exposure,2047,changeExposure)
    cv2.createTrackbar('Sharpness',Window_name,sharpness,255,changeSharpness)
    cv2.createTrackbar('WB temperature',Window_name,wbtemperature,6500,changeSharpness)
    cv2.createTrackbar('Focus',Window_name,focus,250,changeFocus)
    cv2.createTrackbar('Zoom',Window_name,zoom,500,changeZoom)

    while(True):
        # streamture frame-by-frame
        ret, frame = stream.read()
        
        # if the frame was not ret, then we have reached the end
        # of the stream
        if not ret:
            break

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # # Display the resulting frame
        # cv2.imshow(Window_name,gray)
        frame = show_fps(frame, fps)
        # cv2.rectangle(frame, (0, 35), (149, 18), (0, 0, 0), -1)
        cv2.namedWindow(Window_name)
        cv2.imshow(Window_name,frame)
        toc = time.time()
        curr_fps = 1.0 / (toc - tic)
        # calculate an exponentially decaying average of fps number
        fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
        tic = toc

        if cv2.waitKey(1) & 0xFF == 27:
            break

    # When everything done, release the streamture
    stream.release()
    cv2.destroyWindows(Window_name)

if __name__ == "__main__":
    Window_name="Control Camera"
    stream=(cv2.VideoCapture(0, cv2.CAP_V4L2))
    main(stream=stream, Window_name=Window_name)


