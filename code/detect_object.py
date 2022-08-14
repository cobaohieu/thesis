import cv2
import time
import numpy as np


from collections import deque
from time import gmtime, strftime
from datetime import datetime
from math import radians, degrees, cos, sin, tan
from PIL import Image

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

res = '480p'
height = 480
width = 640
# stream = cv2.VideoCapture(0)
global stream

# Standard Video Dimensions Sizes
STD_DIMENSIONS = {"480p" : (640, 480),
                   "720p" : (1280, 720),
                   "1080p": (1920, 1080),
                   "4k"   : (3840, 2160),}

def change_res(stream, width, height):
    stream.set(3, width)
    stream.set(4, height)

# grab resolution dimensions and set video capture to it.
def get_dims(stream, res=res):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    change_res(stream, width, height)
    return width, height

def detect_object(stream, width=width, height=height):
    # Load YOLO
    # net = cv2.dnn.readNet("./weights/yolov3.weights", "./cfg/yolov3.cfg")
    net = cv2.dnn.readNet("./weights/yolov3-custom_final.weights", "./cfg/yolov3-custom.cfg")
    classess = []
    #labels = "./data/coco.names"
    labels = "./data/yolo.names"
    with open(labels, "r") as f:
        classess = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classess), 3))

    # Load image
    # stream = cv2.VideoCapture(0) # 0 for 1st webcam
    stream.set(3, width)
    stream.set(4, height)

    font = cv2.FONT_HERSHEY_PLAIN
    FpsCalc = FpsCalculator(buffer_len = 50)
    # starting_time = time.time()
    # frame_id = 0

    while True:
        display_fps = round(FpsCalc.get(), 3)

        _, frame = stream.read() #
        height,width,channels = frame.shape

        # detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320,320), (0,0,0), True, crop=False) # reduce 416 to 320
        net.setInput(blob)
        outs = net.forward(outputlayers)
        print(len(outs), len)

        # Showing info on screen / get confidens score of algorithm in detecting an object in blob
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # onject detected
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    # rectangle co-ordinaters
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    # cv2.rectangle(img, (x,y), (x+y, y+h), (0,255,0),2)
                    boxes.append([x,y,w,h]) # put all rectangle areas
                    confidences.append(float(confidence)) # how confidence was that object detected and show that percentage
                    class_ids.append(class_id) # name of the object that was detected

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

        for i in range(len(boxes)):
            if i in indexes:
                x,y,w,h = boxes[i]
                label = str(classess[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
                cv2.putText(frame,label+" "+str(round(confidence,2)),(x,y-5),font,1,(255,255,255),2)

        # puting the FPS count on the frame
        cv2.putText(frame, "FPS:" + str(display_fps), ((width-150), 30),
                    font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
        # elapsed_time = time.time() - starting_time
        # fps = frame_id/elapsed_time
        # cv2.putText(frame, "FPS: "+str(round(fps,2)), (10,50), font,2,(0,0,0),1)

        cv2.imshow("Detect Object mode", frame)
        key = cv2.waitKey(1) # Wait 1ms the loop will start again and we will process the next frame
        if key == 27: # ESC key stops the process
            break;

    stream.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_object(stream = cv2.VideoCapture(0))
