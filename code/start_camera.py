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
import OpenGL.GL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import numpy.linalg
import sys
import cv2
import time
from collections import deque
import copy
import argparse
import tkinter as tk

#window dimensions
# 1280x720 | 1600x896 | 1920x1080
# 640x360  |  800x448 | 800x600  | 864x480 | 960x720 | 1024x576
# 160x90   |  160x120 | 176x144  | 320x180 | 320x240 | 352x288

global stream


stream = None
nRange = 1.0
width = 1280
height = 720
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

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

def cv2array(im):
    depth2dtype = {cv2.cv.IPL_DEPTH_8U: 'uint8',
                    cv2.cv.IPL_DEPTH_8S: 'int8',
                    cv2.cv.IPL_DEPTH_16U: 'uint16',
                    cv2.cv.IPL_DEPTH_16S: 'int16',
                    cv2.cv.IPL_DEPTH_32S: 'int32',
                    cv2.cv.IPL_DEPTH_32F: 'float32',
                    cv2.cv.IPL_DEPTH_64F: 'float64',}

    arrdtype=im.depth
    a = np.fromstring(im.tostring(),
                        dtype=depth2dtype[im.depth],
                        count=im.width*im.height*im.nChannels)
    a.shape = (im.height,im.width,im.nChannels)
    return a

def init():
    #glclearcolor (r, g, b, alpha)
    glClearDepth(1.0)
    # glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)

def idle(FpsCalc = FpsCalculator(buffer_len = 50)):
    global stream
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX

    display_fps = round(FpsCalc.get(), 3)

    retval, frame = stream.read()

    # puting the FPS count on the frame
    cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
                font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

    frame = cv2.flip(frame,0)

    image_size =(int(stream.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("Camera resolution: ", image_size)
    # print("Camera fps       : ", cv2.CAP_PROP_FPS)
    print("Camera FPS       : ", display_fps)
    frame = cv2.resize(frame, image_size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # image_arr = cv2array(frame)
    # you must convert the frame to array for glTexImage2D to work
    # maybe there is a faster way that I don't know about yet...
    # print(image_arr)

    # Create Texture
    glTexImage2D(GL_TEXTURE_2D,
                0,
                GL_RGB,
                image_size[0],image_size[1],
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                frame)
    glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, frame)
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    #this one is necessary with texture2d for some reason
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Set Projection Matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    # Switch to Model View Matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Draw textured Quads
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0)
    glVertex2f(0.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex2f(width, 0.0)

    glTexCoord2f(1.0, 1.0)
    glVertex2f(width, height)

    glTexCoord2f(0.0, 1.0)
    glVertex2f(0.0, height)

    glEnd()

    # Render now
    glFlush()
    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # allows for reshaping the window without distoring shape
    if w <= h:
        glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
    else:
        glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    global anim
    key = cv2.waitKey(1)
    if key == 27:
        stream.release()
        stream.destroyAllWindows()
    return
        # quit()

def display_camera():
    global stream
    stream = cv2.VideoCapture(0)

    FpsCalc = FpsCalculator(buffer_len = 50)
    while stream.isOpened():
        glutInit(sys.argv)
        # glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        windows_width = (screen_width - width) // 2
        windows_height = (screen_height - height) // 2
        glutInitWindowPosition(windows_width, windows_height)
        # glutInitWindowPosition(int((glutGet(GLUT_SCREEN_WIDTH)-1366)/2),
        #                        int((glutGet(GLUT_SCREEN_HEIGHT)-768)/2))
        glutCreateWindow("Camera view")

        init()
        glutMainLoop()

if __name__ == "__main__":
    display_camera()