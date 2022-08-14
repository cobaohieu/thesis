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
import os
import datetime
import time
import cv2
import numpy as np
import numpy.linalg

################## Modules path ##################
sys.path.append(os.path.join(os.path.dirname(__file__), "./"))


# import config_ui

################## Import sub modules ##################
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from PIL import Image
from imutils.video import VideoStream
from screeninfo import get_monitors

from pyzbar import pyzbar
from pyzbar.pyzbar import decode

from collections import OrderedDict
from collections import deque

# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *


date = datetime.now()
path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.sep + 'output/video_%s%s%sT%s%s%s.mp4'%(date.year, date.month, date.day, date.hour, date.minute, date.second)
frames_per_second = 24.0
res = '480p'
width = 640
# stream = cv2.VideoCapture(0)
global stream

# Standard Video Dimensions Sizes
STD_DIMENSIONS = {"480p" : (640, 480),
                   "720p" : (1280, 720),
                   "1080p": (1920, 1080),
                   "4k"   : (3840, 2160),}


def blur(frame):
     # some intensive computation...
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    return frame

def mono(frame):
    frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame

def hue(frame):
    frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    return frame

def invert(stream):
    frame =  cv2.bitwise_not(frame)
    return frame
        
def rotate_x_axis(frame):
    frame = cv2.flip(frame, 0)
    return frame

### def mirror is the same def rotate_y_axis
def rotate_y_axis(frame):
    frame = cv2.flip(frame, 1)
    return frame

def rotate_both_axis(frame):
    frame = cv2.flip(frame, -1)
    return frame

def clear_camera(stream, out):
    stream.release()
    out.release()
    cv2.destroyAllWindows()

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
    width, height = STD_DIMENSIONS["480p"]
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
    # 'mp4': cv2.VideoWriter_fourcc(*'MJPG'),
    # 'mp4': cv2.VideoWriter_fourcc('M','J','P','G'),
    # 'mp4': cv2.VideoWriter_fourcc(*'X264'),
    # 'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    'mkv': cv2.VideoWriter_fourcc(*'X264')}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

class CameraControl():
    def setting_camera(self):
        WINDOW_NAME = 'Record video mode'
        stream = cv2.VideoCapture(0, cv2.CAP_V4L)
        properties = ["CAP_PROP_FRAME_WIDTH",  # Width of the frames in the video stream.
                      "CAP_PROP_FRAME_HEIGHT", # Height of the frames in the video stream.
                      "CAP_PROP_BRIGHTNESS",   # Brightness of the image (only for cameras).
                      "CAP_PROP_CONTRAST",     # Contrast of the image (only for cameras).
                      "CAP_PROP_SATURATION",   # Saturation of the image (only for cameras).
                    #   "CAP_PROP_HUE",           # Hue of the image (only for cameras)
                      "CAP_PROP_GAIN",          # Gain of the image (only for cameras).
                      "CAP_PROP_EXPOSURE",      # Exposure (only for cameras)
                      "CAP_PROP_SHARPNESS",
                    #   "CAP_PROP_GAMMA",
                    #   "CAP_PROP_TEMPERATURE",
                      "CAP_PROP_ZOOM",
                      "CAP_PROP_FOCUS",]
                    #   "CAP_PROP_PAN",
                    #   "CAP_PROP_TILT",]


        # set a lower resolution for speed up
        stream.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        # env variables
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW_NAME, 640, 480)
        cv2.moveWindow(WINDOW_NAME, 0, 0)
        cv2.setWindowTitle(WINDOW_NAME, WINDOW_NAME)

        full_screen = False

        for prop in properties:
            val = stream.get(eval("cv2." + prop))
            print (prop + ": " + str(val))

        # stream.set(cv2.CAP_PROP_CONVERT_RGB, 32) # output the frame as a 2D matrix instead of 3D matrix
        # stream.set(cv2.CAP_PROP_MONOCHROME, True) # expect monochrome output from camera

        brightness = 128 # 140
        stream.set(cv2.CAP_PROP_BRIGHTNESS, brightness)

        contrast = 128 # 130
        stream.set(cv2.CAP_PROP_CONTRAST, contrast)

        saturation = 128 # 130
        stream.set(cv2.CAP_PROP_SATURATION, saturation)

        # hue = 200
        # stream.set(cv2.CAP_PROP_HUE, hue)

        gain = 0 # 25
        stream.set(cv2.CAP_PROP_GAIN, gain)

        exposure = 1200 # 500
        stream.set(cv2.CAP_PROP_EXPOSURE, exposure)

        sharpness = 128 # 50
        stream.set(cv2.CAP_PROP_SHARPNESS, sharpness)

        # gamma = 50
        # stream.set(cv2.CAP_PROP_GAMMA, gamma)
	
	    # 2000 - 6500
        # temperature = 4500
        # stream.set(cv2.CAP_PROP_TEMPERATURE, temperature)

        zoom = 100
        stream.set(cv2.CAP_PROP_ZOOM, zoom)

        focus = 25
        stream.set(cv2.CAP_PROP_FOCUS, focus)

        # pan = 0
        # stream.set(cv2.CAP_PROP_PAN, pan)

        # tilt = 0
        # stream.set(cv2.CAP_PROP_TILT,tilt)

        while(True):
            # Capture frame-by-frame
            ret, frame = stream.read()

            # Our operations on the frame come here
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # rgb = frame

            print ("\n\n")
            for prop in properties:
                val = stream.get(eval("cv2." + prop))
                print (prop + ": " + str(val))

            # Display the resulting frame
            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:  # exit
                break
            elif key == 190: # F1
                brightness += 1
                stream.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
            elif key == 191: # F2
                brightness -= 1
                stream.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
            elif key == 192: # F3
                contrast += 1
                stream.set(cv2.CAP_PROP_CONTRAST, contrast)
            elif key == 193: # F4
                contrast -= 1
                stream.set(cv2.CAP_PROP_CONTRAST, contrast)
            elif key == 194: # F5
                saturation += 1
                stream.set(cv2.CAP_PROP_SATURATION, saturation)
            elif key == 195: # F6
                saturation -= 1
                stream.set(cv2.CAP_PROP_SATURATION, saturation)
            # elif key == ord('e'):
            #     hue += 1
            #     stream.set(cv2.CAP_PROP_HUE, hue)
            # elif key == ord('r'):
            #     hue -= 1
            #     stream.set(cv2.CAP_PROP_HUE, hue)
            elif key == 196: # F7
                gain += 1
                stream.set(cv2.CAP_PROP_GAIN, gain)
            elif key == 197: # F8
                gain -= 1
                stream.set(cv2.CAP_PROP_GAIN, gain)
            elif key == 198: # F9
                exposure += 1
                stream.set(cv2.CAP_PROP_EXPOSURE, exposure)
            elif key == 199: # F10
                exposure -= 1
                stream.set(cv2.CAP_PROP_EXPOSURE, exposure)
            elif key == 200: # F11
                sharpness += 1
                stream.set(cv2.CAP_PROP_SHARPNESS, sharpness)
            elif key == 201: # F12
                sharpness -= 1
                stream.set(cv2.CAP_PROP_SHARPNESS, sharpness)
            # elif key == ord('g'):
            #     gamma += 1
            #     stream.set(cv2.CAP_PROP_GAMMA, gamma)
            # elif key == ord('h'):
            #     gamma -= 1
            #     stream.set(cv2.CAP_PROP_GAMMA, gamma)
            # elif key == ord('q'):
            #     temperature += 1
            #     stream.set(cv2.CAP_PROP_TEMPERATURE, temperature)
            # elif key == ord('e'):
            #     temperature -= 1
            #     stream.set(cv2.CAP_PROP_TEMPERATURE, temperature)
            elif key == ord('a'):
                zoom += 1
                stream.set(cv2.CAP_PROP_ZOOM, zoom)
            elif key == ord('d'):
                zoom -= 1
                stream.set(cv2.CAP_PROP_ZOOM, zoom)
            elif key == ord('w'):
                focus += 1
                stream.set(cv2.CAP_PROP_FOCUS, focus)
            elif key == ord('s'):
                focus -= 1
                stream.set(cv2.CAP_PROP_FOCUS, focus)
            # elif key == 83:
            #     pan += 1
            #     stream.set(cv2.CAP_PROP_PAN, pan)
            # elif key == 81:
            #     pan -= 1
            #     stream.set(cv2.CAP_PROP_PAN, pan)
            # elif key == 82:
            #     tilt += 1
            #     stream.set(cv2.CAP_PROP_TILT, tilt)
            # elif key == 84:
            #     tilt -= 1
            #     stream.set(cv2.CAP_PROP_TILT, tilt)
            elif key == ord('F') or key == ord('f'): # or key == 200:  # full screen
                print('Changing full screen option!')
                full_screen = not full_screen
                if full_screen:
                    print('Setting FS!!!')
                    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                                            cv2.WINDOW_FULLSCREEN)
                else:
                    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                                            cv2.WINDOW_NORMAL)
            else:
                print(key)

        # When everything done, release the capture
        stream.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # rotate_x_axis(stream = cv2.VideoCapture(0))
    controlCamera = CameraControl()
    controlCamera.setting_camera()


#     -4 | cv2.CAP_PROP_DC1394_OFF
#     -3 | cv2.CAP_PROP_DC1394_MODE_MANUAL
#     -2 | cv2.CAP_PROP_DC1394_MODE_AUTO
#     -1 | cv2.CAP_PROP_DC1394_MODE_ONE_PUSH_AUTO
#      0 | cv2.CAP_PROP_POS_MSEC
#      1 | cv2.CAP_PROP_POS_FRAMES
#      2 | cv2.CAP_PROP_POS_AVI_RATIO
#      3 | cv2.CAP_PROP_FRAME_WIDTH
#      4 | cv2.CAP_PROP_FRAME_HEIGHT
#      5 | cv2.CAP_PROP_FPS
#      6 | cv2.CAP_PROP_FOURCC
#      7 | cv2.CAP_PROP_FRAME_COUNT
#      8 | cv2.CAP_PROP_FORMAT
#      9 | cv2.CAP_PROP_MODE
#     10 | cv2.CAP_PROP_BRIGHTNESS
#     11 | cv2.CAP_PROP_CONTRAST
#     12 | cv2.CAP_PROP_SATURATION
#     13 | cv2.CAP_PROP_HUE
#     14 | cv2.CAP_PROP_GAIN
#     15 | cv2.CAP_PROP_EXPOSURE
#     16 | cv2.CAP_PROP_CONVERT_RGB
#     17 | cv2.CAP_PROP_WHITE_BALANCE_BLUE_U
#     18 | cv2.CAP_PROP_RECTIFICATION
#     19 | cv2.CAP_PROP_MONOCHROME
#     20 | cv2.CAP_PROP_SHARPNESS
#     21 | cv2.CAP_PROP_AUTO_EXPOSURE
#     22 | cv2.CAP_PROP_GAMMA
#     23 | cv2.CAP_PROP_TEMPERATURE
#     24 | cv2.CAP_PROP_TRIGGER
#     25 | cv2.CAP_PROP_TRIGGER_DELAY
#     26 | cv2.CAP_PROP_WHITE_BALANCE_RED_V
#     27 | cv2.CAP_PROP_ZOOM
#     28 | cv2.CAP_PROP_FOCUS
#     29 | cv2.CAP_PROP_GUID
#     30 | cv2.CAP_PROP_ISO_SPEED
#     31 | cv2.CAP_PROP_DC1394_MAX
#     32 | cv2.CAP_PROP_BACKLIGHT
#     33 | cv2.CAP_PROP_PAN
#     34 | cv2.CAP_PROP_TILT
#     35 | cv2.CAP_PROP_ROLL
#     36 | cv2.CAP_PROP_IRIS
#     37 | cv2.CAP_PROP_SETTINGS
#     38 | cv2.CAP_PROP_BUFFERSIZE
#     39 | cv2.CAP_PROP_AUTOFOCUS
#     40 | cv2.CAP_PROP_SAR_NUM
#     41 | cv2.CAP_PROP_SAR_DEN
#     42 | cv2.CAP_PROP_BACKEND
#     43 | cv2.CAP_PROP_CHANNEL
#     44 | cv2.CAP_PROP_AUTO_WB
#     45 | cv2.CAP_PROP_WB_TEMPERATURE
#     46 | cv2.CAP_PROP_CODEC_PIXEL_FORMAT
#     47 | cv2.CAP_PROP_BITRATE
#    100 | cv2.CAP_PROP_OPENNI_OUTPUT_MODE
#    101 | cv2.CAP_PROP_OPENNI_FRAME_MAX_DEPTH
#    102 | cv2.CAP_PROP_OPENNI_BASELINE
#    103 | cv2.CAP_PROP_OPENNI_FOCAL_LENGTH
#    104 | cv2.CAP_PROP_OPENNI_REGISTRATION
#    104 | cv2.CAP_PROP_OPENNI_REGISTRATION_ON
#    105 | cv2.CAP_PROP_OPENNI_APPROX_FRAME_SYNC
#    106 | cv2.CAP_PROP_OPENNI_MAX_BUFFER_SIZE
#    107 | cv2.CAP_PROP_OPENNI_CIRCLE_BUFFER
#    108 | cv2.CAP_PROP_OPENNI_MAX_TIME_DURATION
#    109 | cv2.CAP_PROP_OPENNI_GENERATOR_PRESENT
#    110 | cv2.CAP_PROP_OPENNI2_SYNC
#    111 | cv2.CAP_PROP_OPENNI2_MIRROR
#    200 | cv2.CAP_PROP_GSTREAMER_QUEUE_LENGTH
#    300 | cv2.CAP_PROP_PVAPI_MULTICASTIP
#    301 | cv2.CAP_PROP_PVAPI_FRAMESTARTTRIGGERMODE
#    302 | cv2.CAP_PROP_PVAPI_DECIMATIONHORIZONTAL
#    303 | cv2.CAP_PROP_PVAPI_DECIMATIONVERTICAL
#    304 | cv2.CAP_PROP_PVAPI_BINNINGX
#    305 | cv2.CAP_PROP_PVAPI_BINNINGY
#    306 | cv2.CAP_PROP_PVAPI_PIXELFORMAT
#    400 | cv2.CAP_PROP_XI_DOWNSAMPLING
#    401 | cv2.CAP_PROP_XI_DATA_FORMAT
#    402 | cv2.CAP_PROP_XI_OFFSET_X
#    403 | cv2.CAP_PROP_XI_OFFSET_Y
#    404 | cv2.CAP_PROP_XI_TRG_SOURCE
#    405 | cv2.CAP_PROP_XI_TRG_SOFTWARE
#    406 | cv2.CAP_PROP_XI_GPI_SELECTOR
#    407 | cv2.CAP_PROP_XI_GPI_MODE
#    408 | cv2.CAP_PROP_XI_GPI_LEVEL
#    409 | cv2.CAP_PROP_XI_GPO_SELECTOR
#    410 | cv2.CAP_PROP_XI_GPO_MODE
#    411 | cv2.CAP_PROP_XI_LED_SELECTOR
#    412 | cv2.CAP_PROP_XI_LED_MODE
#    413 | cv2.CAP_PROP_XI_MANUAL_WB
#    414 | cv2.CAP_PROP_XI_AUTO_WB
#    415 | cv2.CAP_PROP_XI_AEAG
#    416 | cv2.CAP_PROP_XI_EXP_PRIORITY
#    417 | cv2.CAP_PROP_XI_AE_MAX_LIMIT
#    418 | cv2.CAP_PROP_XI_AG_MAX_LIMIT
#    419 | cv2.CAP_PROP_XI_AEAG_LEVEL
#    420 | cv2.CAP_PROP_XI_TIMEOUT
#    421 | cv2.CAP_PROP_XI_EXPOSURE
#    422 | cv2.CAP_PROP_XI_EXPOSURE_BURST_COUNT
#    423 | cv2.CAP_PROP_XI_GAIN_SELECTOR
#    424 | cv2.CAP_PROP_XI_GAIN
#    426 | cv2.CAP_PROP_XI_DOWNSAMPLING_TYPE
#    427 | cv2.CAP_PROP_XI_BINNING_SELECTOR
#    428 | cv2.CAP_PROP_XI_BINNING_VERTICAL
#    429 | cv2.CAP_PROP_XI_BINNING_HORIZONTAL
#    430 | cv2.CAP_PROP_XI_BINNING_PATTERN
#    431 | cv2.CAP_PROP_XI_DECIMATION_SELECTOR
#    432 | cv2.CAP_PROP_XI_DECIMATION_VERTICAL
#    433 | cv2.CAP_PROP_XI_DECIMATION_HORIZONTAL
#    434 | cv2.CAP_PROP_XI_DECIMATION_PATTERN
#    435 | cv2.CAP_PROP_XI_IMAGE_DATA_FORMAT
#    436 | cv2.CAP_PROP_XI_SHUTTER_TYPE
#    437 | cv2.CAP_PROP_XI_SENSOR_TAPS
#    439 | cv2.CAP_PROP_XI_AEAG_ROI_OFFSET_X
#    440 | cv2.CAP_PROP_XI_AEAG_ROI_OFFSET_Y
#    441 | cv2.CAP_PROP_XI_AEAG_ROI_WIDTH
#    442 | cv2.CAP_PROP_XI_AEAG_ROI_HEIGHT
#    445 | cv2.CAP_PROP_XI_BPC
#    448 | cv2.CAP_PROP_XI_WB_KR
#    449 | cv2.CAP_PROP_XI_WB_KG
#    450 | cv2.CAP_PROP_XI_WB_KB
#    451 | cv2.CAP_PROP_XI_WIDTH
#    452 | cv2.CAP_PROP_XI_HEIGHT
#    459 | cv2.CAP_PROP_XI_LIMIT_BANDWIDTH
#    460 | cv2.CAP_PROP_XI_SENSOR_DATA_BIT_DEPTH
#    461 | cv2.CAP_PROP_XI_OUTPUT_DATA_BIT_DEPTH
#    462 | cv2.CAP_PROP_XI_IMAGE_DATA_BIT_DEPTH
#    463 | cv2.CAP_PROP_XI_OUTPUT_DATA_PACKING
#    464 | cv2.CAP_PROP_XI_OUTPUT_DATA_PACKING_TYPE
#    465 | cv2.CAP_PROP_XI_IS_COOLED
#    466 | cv2.CAP_PROP_XI_COOLING
#    467 | cv2.CAP_PROP_XI_TARGET_TEMP
#    468 | cv2.CAP_PROP_XI_CHIP_TEMP
#    469 | cv2.CAP_PROP_XI_HOUS_TEMP
#    470 | cv2.CAP_PROP_XI_CMS
#    471 | cv2.CAP_PROP_XI_APPLY_CMS
#    474 | cv2.CAP_PROP_XI_IMAGE_IS_COLOR
#    475 | cv2.CAP_PROP_XI_COLOR_FILTER_ARRAY
#    476 | cv2.CAP_PROP_XI_GAMMAY
#    477 | cv2.CAP_PROP_XI_GAMMAC
#    478 | cv2.CAP_PROP_XI_SHARPNESS
#    479 | cv2.CAP_PROP_XI_CC_MATRIX_00
#    480 | cv2.CAP_PROP_XI_CC_MATRIX_01
#    481 | cv2.CAP_PROP_XI_CC_MATRIX_02
#    482 | cv2.CAP_PROP_XI_CC_MATRIX_03
#    483 | cv2.CAP_PROP_XI_CC_MATRIX_10
#    484 | cv2.CAP_PROP_XI_CC_MATRIX_11
#    485 | cv2.CAP_PROP_XI_CC_MATRIX_12
#    486 | cv2.CAP_PROP_XI_CC_MATRIX_13
#    487 | cv2.CAP_PROP_XI_CC_MATRIX_20
#    488 | cv2.CAP_PROP_XI_CC_MATRIX_21
#    489 | cv2.CAP_PROP_XI_CC_MATRIX_22
#    490 | cv2.CAP_PROP_XI_CC_MATRIX_23
#    491 | cv2.CAP_PROP_XI_CC_MATRIX_30
#    492 | cv2.CAP_PROP_XI_CC_MATRIX_31
#    493 | cv2.CAP_PROP_XI_CC_MATRIX_32
#    494 | cv2.CAP_PROP_XI_CC_MATRIX_33
#    495 | cv2.CAP_PROP_XI_DEFAULT_CC_MATRIX
#    498 | cv2.CAP_PROP_XI_TRG_SELECTOR
#    499 | cv2.CAP_PROP_XI_ACQ_FRAME_BURST_COUNT
#    507 | cv2.CAP_PROP_XI_DEBOUNCE_EN
#    508 | cv2.CAP_PROP_XI_DEBOUNCE_T0
#    509 | cv2.CAP_PROP_XI_DEBOUNCE_T1
#    510 | cv2.CAP_PROP_XI_DEBOUNCE_POL
#    511 | cv2.CAP_PROP_XI_LENS_MODE
#    512 | cv2.CAP_PROP_XI_LENS_APERTURE_VALUE
#    513 | cv2.CAP_PROP_XI_LENS_FOCUS_MOVEMENT_VALUE
#    514 | cv2.CAP_PROP_XI_LENS_FOCUS_MOVE
#    515 | cv2.CAP_PROP_XI_LENS_FOCUS_DISTANCE
#    516 | cv2.CAP_PROP_XI_LENS_FOCAL_LENGTH
#    517 | cv2.CAP_PROP_XI_LENS_FEATURE_SELECTOR
#    518 | cv2.CAP_PROP_XI_LENS_FEATURE
#    521 | cv2.CAP_PROP_XI_DEVICE_MODEL_ID
#    522 | cv2.CAP_PROP_XI_DEVICE_SN
#    529 | cv2.CAP_PROP_XI_IMAGE_DATA_FORMAT_RGB32_ALPHA
#    530 | cv2.CAP_PROP_XI_IMAGE_PAYLOAD_SIZE
#    531 | cv2.CAP_PROP_XI_TRANSPORT_PIXEL_FORMAT
#    532 | cv2.CAP_PROP_XI_SENSOR_CLOCK_FREQ_HZ
#    533 | cv2.CAP_PROP_XI_SENSOR_CLOCK_FREQ_INDEX
#    534 | cv2.CAP_PROP_XI_SENSOR_OUTPUT_CHANNEL_COUNT
#    535 | cv2.CAP_PROP_XI_FRAMERATE
#    536 | cv2.CAP_PROP_XI_COUNTER_SELECTOR
#    537 | cv2.CAP_PROP_XI_COUNTER_VALUE
#    538 | cv2.CAP_PROP_XI_ACQ_TIMING_MODE
#    539 | cv2.CAP_PROP_XI_AVAILABLE_BANDWIDTH
#    540 | cv2.CAP_PROP_XI_BUFFER_POLICY
#    541 | cv2.CAP_PROP_XI_LUT_EN
#    542 | cv2.CAP_PROP_XI_LUT_INDEX
#    543 | cv2.CAP_PROP_XI_LUT_VALUE
#    544 | cv2.CAP_PROP_XI_TRG_DELAY
#    545 | cv2.CAP_PROP_XI_TS_RST_MODE
#    546 | cv2.CAP_PROP_XI_TS_RST_SOURCE
#    547 | cv2.CAP_PROP_XI_IS_DEVICE_EXIST
#    548 | cv2.CAP_PROP_XI_ACQ_BUFFER_SIZE
#    549 | cv2.CAP_PROP_XI_ACQ_BUFFER_SIZE_UNIT
#    550 | cv2.CAP_PROP_XI_ACQ_TRANSPORT_BUFFER_SIZE
#    551 | cv2.CAP_PROP_XI_BUFFERS_QUEUE_SIZE
#    552 | cv2.CAP_PROP_XI_ACQ_TRANSPORT_BUFFER_COMMIT
#    553 | cv2.CAP_PROP_XI_RECENT_FRAME
#    554 | cv2.CAP_PROP_XI_DEVICE_RESET
#    555 | cv2.CAP_PROP_XI_COLUMN_FPN_CORRECTION
#    558 | cv2.CAP_PROP_XI_SENSOR_MODE
#    559 | cv2.CAP_PROP_XI_HDR
#    560 | cv2.CAP_PROP_XI_HDR_KNEEPOINT_COUNT
#    561 | cv2.CAP_PROP_XI_HDR_T1
#    562 | cv2.CAP_PROP_XI_HDR_T2
#    563 | cv2.CAP_PROP_XI_KNEEPOINT1
#    564 | cv2.CAP_PROP_XI_KNEEPOINT2
#    565 | cv2.CAP_PROP_XI_IMAGE_BLACK_LEVEL
#    571 | cv2.CAP_PROP_XI_HW_REVISION
#    572 | cv2.CAP_PROP_XI_DEBUG_LEVEL
#    573 | cv2.CAP_PROP_XI_AUTO_BANDWIDTH_CALCULATION
#    580 | cv2.CAP_PROP_XI_FFS_FILE_SIZE
#    581 | cv2.CAP_PROP_XI_FREE_FFS_SIZE
#    582 | cv2.CAP_PROP_XI_USED_FFS_SIZE
#    583 | cv2.CAP_PROP_XI_FFS_ACCESS_KEY
#    585 | cv2.CAP_PROP_XI_SENSOR_FEATURE_SELECTOR
#    586 | cv2.CAP_PROP_XI_SENSOR_FEATURE_VALUE
#    587 | cv2.CAP_PROP_XI_TEST_PATTERN_GENERATOR_SELECTOR
#    588 | cv2.CAP_PROP_XI_TEST_PATTERN
#    589 | cv2.CAP_PROP_XI_REGION_SELECTOR
#    590 | cv2.CAP_PROP_XI_HOUS_BACK_SIDE_TEMP
#    591 | cv2.CAP_PROP_XI_ROW_FPN_CORRECTION
#    594 | cv2.CAP_PROP_XI_FFS_FILE_ID
#    595 | cv2.CAP_PROP_XI_REGION_MODE
#    596 | cv2.CAP_PROP_XI_SENSOR_BOARD_TEMP
#    600 | cv2.CAP_PROP_ARAVIS_AUTOTRIGGER
#   9001 | cv2.CAP_PROP_IOS_DEVICE_FOCUS
#   9002 | cv2.CAP_PROP_IOS_DEVICE_EXPOSURE
#   9003 | cv2.CAP_PROP_IOS_DEVICE_FLASH
#   9004 | cv2.CAP_PROP_IOS_DEVICE_WHITEBALANCE
#   9005 | cv2.CAP_PROP_IOS_DEVICE_TORCH
#  10001 | cv2.CAP_PROP_GIGA_FRAME_OFFSET_X
#  10002 | cv2.CAP_PROP_GIGA_FRAME_OFFSET_Y
#  10003 | cv2.CAP_PROP_GIGA_FRAME_WIDTH_MAX
#  10004 | cv2.CAP_PROP_GIGA_FRAME_HEIGH_MAX
#  10005 | cv2.CAP_PROP_GIGA_FRAME_SENS_WIDTH
#  10006 | cv2.CAP_PROP_GIGA_FRAME_SENS_HEIGH
#  11001 | cv2.CAP_PROP_INTELPERC_PROFILE_COUNT
#  11002 | cv2.CAP_PROP_INTELPERC_PROFILE_IDX
#  11003 | cv2.CAP_PROP_INTELPERC_DEPTH_LOW_CONFIDENCE_VALUE
#  11004 | cv2.CAP_PROP_INTELPERC_DEPTH_SATURATION_VALUE
#  11005 | cv2.CAP_PROP_INTELPERC_DEPTH_CONFIDENCE_THRESHOLD
#  11006 | cv2.CAP_PROP_INTELPERC_DEPTH_FOCAL_LENGTH_HORZ
#  11007 | cv2.CAP_PROP_INTELPERC_DEPTH_FOCAL_LENGTH_VERT
#  17001 | cv2.CAP_PROP_GPHOTO2_PREVIEW
#  17002 | cv2.CAP_PROP_GPHOTO2_WIDGET_ENUMERATE
#  17003 | cv2.CAP_PROP_GPHOTO2_RELOAD_CONFIG
#  17004 | cv2.CAP_PROP_GPHOTO2_RELOAD_ON_CHANGE
#  17005 | cv2.CAP_PROP_GPHOTO2_COLLECT_MSGS
#  17006 | cv2.CAP_PROP_GPHOTO2_FLUSH_MSGS
#  17007 | cv2.CAP_PROP_SPEED
#  17008 | cv2.CAP_PROP_APERTURE
#  17009 | cv2.CAP_PROP_EXPOSUREPROGRAM
#  17010 | cv2.CAP_PROP_VIEWFINDER
#  18000 | cv2.CAP_PROP_IMAGES_BASE
#  19000 | cv2.CAP_PROP_IMAGES_LAST

# cv2.CAP_PROP_POS_MSEC = 0
# cv2.CAP_PROP_POS_FRAMES = 1
# cv2.CAP_PROP_POS_AVI_RATIO = 2
# cv2.CAP_PROP_FRAME_WIDTH = 3
# cv2.CAP_PROP_FRAME_HEIGHT = 4
# cv2.CAP_PROP_FPS = 5
# cv2.CAP_PROP_FOURCC = 6
# cv2.CAP_PROP_FRAME_COUNT = 7
# cv2.CAP_PROP_FORMAT = 8
# cv2.CAP_PROP_MODE = 9
# cv2.CAP_PROP_BRIGHTNESS = 10
# cv2.CAP_PROP_CONTRAST = 11
# cv2.CAP_PROP_SATURATION = 12
# cv2.CAP_PROP_HUE = 13
# cv2.CAP_PROP_GAIN = 14
# cv2.CAP_PROP_EXPOSURE = 15
# cv2.CAP_PROP_CONVERT_RGB = 16
# cv2.CAP_PROP_WHITE_BALANCE_BLUE_U = 17
# cv2.CAP_PROP_RECTIFICATION = 18
# cv2.CAP_PROP_MONOCHROME = 19
# cv2.CAP_PROP_SHARPNESS = 20
# cv2.CAP_PROP_AUTO_EXPOSURE = 21
# cv2.CAP_PROP_GAMMA = 22
# cv2.CAP_PROP_TEMPERATURE = 23
# cv2.CAP_PROP_TRIGGER = 24
# cv2.CAP_PROP_TRIGGER_DELAY = 25
# cv2.CAP_PROP_WHITE_BALANCE_RED_V = 26
# cv2.CAP_PROP_ZOOM = 27
# cv2.CAP_PROP_FOCUS = 28
# cv2.CAP_PROP_GUID = 29
# cv2.CAP_PROP_ISO_SPEED = 30
# cv2.CAP_PROP_BACKLIGHT = 32
# cv2.CAP_PROP_PAN = 33
# cv2.CAP_PROP_TILT = 34
# cv2.CAP_PROP_ROLL = 35
# cv2.CAP_PROP_IRIS = 36
# cv2.CAP_PROP_SETTINGS = 37
# cv2.CAP_PROP_BUFFERSIZE = 38
# cv2.CAP_PROP_AUTOFOCUS = 39
# cv2.CAP_PROP_SAR_NUM = 40
# cv2.CAP_PROP_SAR_DEN = 41
# cv2.CAP_PROP_BACKEND = 42
# cv2.CAP_PROP_CHANNEL = 43
# cv2.CAP_PROP_AUTO_WB = 44
# cv2.CAP_PROP_WB_TEMPERATURE = 45
# cv2.CAP_PROP_CODEC_PIXEL_FORMAT = 46
# cv2.CAP_PROP_BITRATE = 47
# cv2.CAP_PROP_ORIENTATION_META = 48
# cv2.CAP_PROP_ORIENTATION_AUTO = 49

# CAP_PROP_POS_MSEC- Vị trí hiện tại của tệp video tính bằng mili giây. Giá trị cờ là 0.
# CAP_PROP_POS_FRAMES - Chỉ số dựa trên 0 của khung được giải mã / chụp tiếp theo. Giá trị cờ là 1.
# CAP_PROP_POS_AVI_RATIO- Vị trí tương đối của tệp video: 0 = đầu phim, 1 = cuối phim. Giá trị cờ là 2.
# CAP_PROP_FRAME_WIDTH- Chiều rộng của các khung hình trong luồng video. Giá trị cờ là 3.
# CAP_PROP_FRAME_HEIGHT- Chiều cao của các khung hình trong luồng video. Giá trị cờ là 4.
# CAP_PROP_FPS- Tỷ lệ khung hình. Giá trị cờ là 5.
# CAP_PROP_FOURCC- Mã 4 ký tự của codec. Giá trị cờ là 6.
# CAP_PROP_FRAME_COUNT- Số khung hình trong tệp video. Giá trị cờ là 7.
# CAP_PROP_FORMAT- Định dạng của các đối tượng Mat được trả về VideoCapture. Đặt giá trị -1 để tìm nạp các luồng video RAW chưa được giải mã. Giá trị cờ là 8.
# CAP_PROP_MODE- Giá trị phụ trợ cụ thể cho biết chế độ chụp hiện tại. Giá trị cờ là 9.
# CAP_PROP_BRIGHTNESS- Độ sáng của hình ảnh (chỉ dành cho những máy ảnh hỗ trợ). Giá trị cờ là 10.
# CAP_PROP_CONTRAST—Dung lượng của hình ảnh (chỉ dành cho máy ảnh). Giá trị cờ là 11.
# CAP_PROP_SATURATION- Độ bão hòa của hình ảnh (chỉ dành cho máy ảnh). Giá trị cờ là 12.
# CAP_PROP_HUE—Màu của hình ảnh (chỉ dành cho máy ảnh). Giá trị cờ là 13.
# CAP_PROP_GAIN- Tăng hình ảnh (chỉ dành cho những máy ảnh hỗ trợ). Giá trị cờ là 14.
# CAP_PROP_EXPOSURE- Độ phơi sáng của hình ảnh (chỉ dành cho những máy ảnh hỗ trợ). Giá trị cờ là 15.
# CAP_PROP_CONVERT_RGB- Cờ Boolean cho biết liệu hình ảnh có nên được chuyển đổi sang RGB hay không. Giá trị cờ là 16.