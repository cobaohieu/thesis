import cv2
import time
import mediapipe as mp

"""
cap -> stream
img -> frame
"""


class DrawFace():
    def __init__(self, minDetectionConfidence=0.5, minTrackingConfidence=0.5):
        self.minDetectionCon = minDetectionCon
        self.minTrackingConfidence = minTrackingConfidence
        self.mpDraw = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.mp_drawing = mp.solutions.drawing_utils
        self.faceMesh = self.mp_face_mesh(minDetectionConfidence, minTrackingConfidence)

    def drawFace(self, img):
        self.mp_drawing = mp.solutions.drawing_utils
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False
        self.results = self.faceMesh.process(img)

        # Draw the face mesh annotations on the image.
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if self.results.multi_face_landmarks:
            for face_landmarks in self.results.multi_face_landmarks:
                self.mp_drawing.draw_landmarks(
                    image=img,
                    landmark_list=face_landmarks,
                    connections=selmp_face_mesh.FACE_CONNECTIONS,
                    landmark_drawing_spec=self.drawing_spec,
                    connection_drawing_spec=self.drawing_spec)
        return img

class FaceDetector():
    def __init__(self, minDetectionCon = 0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw = True):
        # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # for video
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        # img.flags.writeable = False
        # self.results = face_mesh.process(img)

        self.results = self.faceDetection.process(img)
        # print(results)

        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bouding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                img = self.fancyDraw(img, bbox)

                cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                            (bbox[0], bbox[1] -20), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 2)
        return img, bboxs

    def fancyDraw(self, img, bbox, l = 30, t = 5, rt = 1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left x , y
        cv2.line(img, (x, y), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y - l), (255, 0, 255), t)
        # Top Right x1, y
        cv2.line(img, (x, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x1, y + l), (255, 0, 255), t)
        # Bottom Left x, y1
        cv2.line(img, (x, y), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y - l), (255, 0, 255), t)
        # Bottom Right x1, y
        cv2.line(img, (x, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x1, y + l), (255, 0, 255), t)

def exec_face_mesh():
    # stream = cv2.VideoCapture("video/1.mp4")
    stream = cv2.VideoCapture(0)
    draw_face = DrawFace()
    while stream.isOpened():
        success, img = stream.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        img = DrawFace.drawFace()
        cv2.imshow('MediaPipe FaceMesh', img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    stream.release()

def exec_face_detect():
    # stream = cv2.VideoCapture("video/1.mp4")
    stream = cv2.VideoCapture(0)
    # pTime = 0
    detector = FaceDetector()
    while stream.isOpened():
        success, img = stream.read()
        # img, bboxs = detector.findFaces(img)
        img, bboxs = detector.findFaces(img)
        # print(bboxs)
        # cTime = time.time()
        # fps = 1/ (cTime - pTime)
        # pTime = cv2.putText(img, f'FPS: {int(fps)}', (20, 70),
        #                         cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    stream.release()

if __name__ == "__main__":
    exec_face_detect()