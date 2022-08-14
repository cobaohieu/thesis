import cv2
import acapture
import pyglview
viewer = pyglview.Viewer()
cap = acapture.open(4) # Camera 0,  /dev/video0
def loop():
    check,frame = cap.read() # non-blocking
    # frame = cv2.flip(image,1)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if check:
        viewer.set_image(frame)
viewer.set_loop(loop)
viewer.start()