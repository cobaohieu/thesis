import cv2
import sys

cascPath = sys.argv[0]
faceCascade = cv2.CascadeClassifier(cascPath)


video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# # When everything is done, release the capture
# video_capture.release()
# cv2.destroyAllWindows()

# import cv2

# deviceId = "/dev/video0"

# # videoCaptureApi = cv2.CAP_ANY       # autodetect default API
# videoCaptureApi = cv2.CAP_FFMPEG
# # videoCaptureApi = cv2.CAP_GSTREAMER 
# cap = cv2.VideoCapture("/dev/video2", videoCaptureApi)

# cap = cv2.VideoCapture(deviceId)
# cap.open(deviceId)
# if not cap.isOpened():
#     raise RuntimeError("ERROR! Unable to open camera")

# try:
#     while True:
#         ret, frame = cap.read()
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
# finally:        
#     cap.release()
#     cv2.destroyAllWindows()