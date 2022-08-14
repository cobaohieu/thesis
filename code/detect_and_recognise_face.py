import numpy as np
import cv2
import pickle

face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBHPFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {"person_name": 1}
with open("labels.pickle", 'wb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.item()}

cap = cv2.VideCapture(4)

while(True):
    # Capture frame by frame
    ret, frame = cap.read()
    gray = cv2.ctvColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors = 5)
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        roi_gray = gray[y:y+h, x:x+w] # (ycord_start, ycord_end)
        roi_color = frame[y:y+h, x:x+w]

        # recognize? deep learned model predict keras tensorflow pytorch
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45: # and conf <= 85:
            print(id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_gray)

        color = (255, 0, 0) # BGR 0-255
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)

    # Display the resulting frame
    cv2.imshow('Detect facemode', frame)
    key = cv2.waitKey(20)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()