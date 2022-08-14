import copy
import argparse

import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time

# from utils.cvfpscalc import CvFpsCalc
# from utils import CvFpsCalc

class CvFpsCalc(object):
    def __init__(self, buffer_len=1):
        self._start_tick = cv2.getTickCount()
        self._freq = 1000.0 / cv2.getTickFrequency()
        self._difftimes = deque(maxlen=buffer_len)

    def get(self):
        current_tick = cv2.getTickCount()
        different_time = (current_tick - self._start_tick) * self._freq
        self._start_tick = current_tick

        self._difftimes.append(different_time)

        fps = 1000.0 / (sum(self._difftimes) / len(self._difftimes))
        fps_rounded = round(fps, 3)

        return fps_rounded

######FULLL
min_detection_confidence = 0.5
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence)

# For webcam input:
def main1():
    stream = cv2.VideoCapture(0)
    while stream.isOpened():
        num_frames = 120;
        for i in range(0, num_frames) :
            success, frame = stream.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            frame.flags.writeable = False
            results = face_detection.process(frame)

            # Draw the face detection annotations on the image.
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(frame, detection)
                cv2.imshow('MediaPipe Face Detection', frame)

            # key = cv2.waitKey(1)
            # if key == 27:  # ESC
            #     break
            if cv2.waitKey(5) & 0xFF == 27:
                break
        stream.release()
### FULLL

# # class FaceDetector():
# #     def __init__(self):
# #         self.mp_face_detection = mp.solutions.face_detection
# #         self.mp_drawing = mp.solutions.drawing_utils
# #         self.mpDraw = mp.solutions.drawing_utils

def fancyDraw(frame, bbox, l = 30, t = 5, rt = 1):
    x, y, w, h = bbox
    x1, y1 = x + w, y + h
    cv2.rectangle(frame, bbox, (255, 0, 255), rt)

    # Top Left x , y
    cv2.line(frame, (x, y), (x + l, y1), (255, 0, 255), t)
    cv2.line(frame, (x, y), (x, y - l), (255, 0, 255), t)

    # Top Right x1, y
    cv2.line(frame, (x, y), (x1 - l, y), (255, 0, 255), t)
    cv2.line(frame, (x, y), (x1, y + l), (255, 0, 255), t)

    # Bottom Left x, y1
    cv2.line(frame, (x, y), (x + l, y1), (255, 0, 255), t)
    cv2.line(frame, (x, y), (x, y - l), (255, 0, 255), t)

    # Bottom Right x1, y
    cv2.line(frame, (x, y), (x1 - l, y), (255, 0, 255), t)
    cv2.line(frame, (x, y), (x1, y + l), (255, 0, 255), t)

# # def face_detect_image():
# # # For static images:
# # with mp_face_detection.FaceDetection(
# #     min_detection_confidence=0.5) as face_detection:
# #   for id, file in enumerate(file_list):
# #     frame = cv2.imread(file)
# #     # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
# #     results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

# #     # Draw face detections of each face.
# #     if not results.detections:
# #       continue
# #     annotated_frame = frame.copy()
# #     for detection in results.detections:
# #       print('Nose tip:')
# #       print(mp_face_detection.get_key_point(
# #           detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
# #       mp_drawing.draw_detection(annotated_frame, detection)
# #     cv2.imwrite('/tmp/annotated_frame' + str(id) + '.png', annotated_frame)

def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1,y1 = pt1
    x2,y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

# For webcam input:
def main2():

    stream = cv2.VideoCapture(0)
    stream.set(3, 640) # set video width
    stream.set(4, 480) # set video height

    pTime = 0

    while stream.isOpened():
        success, frame = stream.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frame.flags.writeable = False
        results = face_detection.process(frame)

        # Draw the face detection annotations on the image.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # bboxs = []
        results = face_detection.process(frame)
        if results.detections: # in reseults.face_detection:
            for id, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bouding_box
                bbox = int(bbocC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iwd), int(bboxC.height * ih)
                ih, iw, ic = frame.shape
                bboxs.append([id, bbox, detection.score])
                # if draw:
                frame = fancyDraw(frame, bbox)
                # Fancy draw

                cv2.putText(frame, f'{int(detection.score[0] * 100)}%',
                            (bbox[0], bbox[1] -20), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 2)

        cTime = time.time()
        fps = 1/ (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        cv2.imshow('MediaPipe Face Detection', frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
    stream.release()


def detect(path,img):
    cascade = cv2.CascadeClassifier(path)

    img=cv2.imread(img,1)
    # converting to gray image for faster video processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rects = cascade.detectMultiScale(gray, 1.2, 3,minSize=(50, 50))
    # if at least 1 face detected
    if len(rects) >= 0:
        # Draw a rectangle around the faces
        for (x, y, w, h) in rects:
            draw_border(img, (x, y), (x + w, y + h), (255, 0, 105),4, 15, 10)
        # Display the resulting frame
        cv2.imshow('Face Detection', img)
        # wait for 'c' to close the application
        cv2.waitKey(0)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)

    parser.add_argument('--use_brect', action='store_true')

    args = parser.parse_args()

    return args


def main():
    # 引数解析 #################################################################
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    min_detection_confidence = args.min_detection_confidence

    use_brect = args.use_brect

    # カメラ準備 ###############################################################
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード #############################################################
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        min_detection_confidence=min_detection_confidence)

    # FPS計測モジュール ########################################################
    cvFpsCalc = CvFpsCalc(buffer_len=50)

    while True:
        display_fps = cvFpsCalc.get()

        # カメラキャプチャ #####################################################
        ret, image = cap.read()
        if not ret:
            break
        image = cv2.flip(image, 1)  # ミラー表示
        debug_image = copy.deepcopy(image)

        # 検出実施 #############################################################
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        # 描画 ################################################################
        if results.detections is not None:
            for detection in results.detections:
                # 描画
                debug_image = draw_detection(debug_image, detection)

        cv2.putText(debug_image, "FPS:" + str(display_fps), (5, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

        # キー処理(ESC：終了) #################################################
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

        # 画面反映 #############################################################
        cv2.imshow('MediaPipe Face Detection Demo', debug_image)

    cap.release()
    cv2.destroyAllWindows()


def draw_detection(image, detection):
    image_width, image_height = image.shape[1], image.shape[0]

    #print(detection)
    #print(detection.location_data.relative_keypoints[0])
    #print(detection.location_data.relative_keypoints[1])
    #print(detection.location_data.relative_keypoints[2])
    #print(detection.location_data.relative_keypoints[3])
    #print(detection.location_data.relative_keypoints[4])
    #print(detection.location_data.relative_keypoints[5])

    # バウンディングボックス
    bbox = detection.location_data.relative_bounding_box
    bbox.xmin = int(bbox.xmin * image_width)
    bbox.ymin = int(bbox.ymin * image_height)
    bbox.width = int(bbox.width * image_width)
    bbox.height = int(bbox.height * image_height)

    cv2.rectangle(image, (int(bbox.xmin), int(bbox.ymin)),
                 (int(bbox.xmin + bbox.width), int(bbox.ymin + bbox.height)),
                 (0, 255, 0), 2)

    # スコア・ラベルID
    #cv2.putText(
    #    image,
    #    str(detection.label_id[0]) + ":" + str(round(detection.score[0], 3)),
    #    (int(bbox.xmin), int(bbox.ymin) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
    #    (0, 255, 0), 2, cv2.LINE_AA)

    # キーポイント：右目
    keypoint0 = detection.location_data.relative_keypoints[0]
    keypoint0.x = int(keypoint0.x * image_width)
    keypoint0.y = int(keypoint0.y * image_height)

    #cv2.circle(image, (int(keypoint0.x), int(keypoint0.y)), 5, (0, 255, 0), 2)

    # キーポイント：左目
    keypoint1 = detection.location_data.relative_keypoints[1]
    keypoint1.x = int(keypoint1.x * image_width)
    keypoint1.y = int(keypoint1.y * image_height)

    #cv2.circle(image, (int(keypoint1.x), int(keypoint1.y)), 5, (0, 255, 0), 2)

    # キーポイント：鼻
    keypoint2 = detection.location_data.relative_keypoints[2]
    keypoint2.x = int(keypoint2.x * image_width)
    keypoint2.y = int(keypoint2.y * image_height)

    #cv2.circle(image, (int(keypoint2.x), int(keypoint2.y)), 5, (0, 255, 0), 2)

    # キーポイント：口
    keypoint3 = detection.location_data.relative_keypoints[3]
    keypoint3.x = int(keypoint3.x * image_width)
    keypoint3.y = int(keypoint3.y * image_height)

    #cv2.circle(image, (int(keypoint3.x), int(keypoint3.y)), 5, (0, 255, 0), 2)

    # キーポイント：右耳
    keypoint4 = detection.location_data.relative_keypoints[4]
    keypoint4.x = int(keypoint4.x * image_width)
    keypoint4.y = int(keypoint4.y * image_height)

    #cv2.circle(image, (int(keypoint4.x), int(keypoint4.y)), 5, (0, 255, 0), 2)

    # キーポイント：左耳
    keypoint5 = detection.location_data.relative_keypoints[5]
    keypoint5.x = int(keypoint5.x * image_width)
    keypoint5.y = int(keypoint5.y * image_height)

    #cv2.circle(image, (int(keypoint5.x), int(keypoint5.y)), 5, (0, 255, 0), 2)

    return image


if __name__ == "__main__":
    main()
